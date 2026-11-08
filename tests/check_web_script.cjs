// Exercise request/animation ownership without launching a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const source = fs.readFileSync('visualization/webapp/templates/main.html', 'utf8')
    .match(/<script>([\s\S]*?)<\/script>/)[1];

function harness(fetch) {
    const elements = new Map();
    class Element {
        constructor() { this.children = []; this.style = {}; this.checked = false; }
        set id(value) { this._id = value; elements.set(value, this); }
        get id() { return this._id; }
        appendChild(child) { this.children.push(child); }
        replaceChildren() { this.children = []; }
    }
    for (const id of ['status', 'board-container', 'initial-state', 'goal-state',
                      'live-switch', 'run', 'reset']) {
        const element = new Element();
        element.id = id;
    }
    const context = vm.createContext({
        document: {getElementById: id => elements.get(id), createElement: () => new Element()},
        setTimeout: fn => queueMicrotask(fn), fetch, console, encodeURIComponent,
    });
    vm.runInContext(source, context);
    vm.runInContext('setBoardSize(5)', context);
    return {context, elements};
}

async function main() {
    {
        const calls = [];
        let resolveStart;
        const start = new Promise(resolve => resolveStart = resolve);
        const {context, elements} = harness((url, options) => {
            calls.push([url, options]);
            return url.startsWith('/run') ? start : Promise.resolve({ok: true});
        });
        assert.equal(elements.get('board-container').children.length, 5);
        const running = vm.runInContext('run()', context);
        vm.runInContext('stopSearch()', context);
        resolveStart({ok: true, json: async () => ({job_id: 'stale'})});
        await running;
        assert(calls.some(([url, options]) => url === '/cancel/stale' && options.method === 'POST'));
        assert(!calls.some(([url]) => url.startsWith('/poll')));
        assert(elements.get('status').textContent.startsWith('Reset.'));
    }
    {
        const finalState = {'p0-0': 1, 'p0-1': 0, 'p1-1': 0};
        const {context, elements} = harness(async url => ({ok: true, json: async () =>
            url.startsWith('/run') ? {job_id: 'solved'} : {
                status: 'solved', live: false, state: finalState, states: [finalState],
            }}));
        await vm.runInContext('run()', context);
        assert.equal(elements.get('status').textContent, 'Solved in 1 jumps.');
        assert.equal(elements.get('p0-0').style.display, 'block');
        assert.equal(elements.get('p0-1').style.display, 'none');
        vm.runInContext('setBoardSize(0)', context);
        assert.equal(elements.get('run').disabled, true);
    }
    console.log('Passed: stale start cancellation, non-live replay, invalid board handling.');
}

main().catch(error => { console.error(error); process.exitCode = 1; });

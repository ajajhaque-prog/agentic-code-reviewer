// Advanced JS: insecure serialization, prototype pollution, insecure eval in node
const vm = require('vm');
const fs = require('fs');

function loadConfig(path) {
    return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function runUser(code) {
    // dangerously using vm with user code without context isolation
    vm.runInThisContext(code); 
}

// insecure merging leading to prototype pollution
function merge(a, b) {
    for (let k in b) a[k] = b[k];
    return a;
}

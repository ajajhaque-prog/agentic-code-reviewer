// bad_js.js
function processUser(input) {
    // TODO: Validate input
    eval("console.log(" + input + ")"); // Security risk
    
    var x = 10;
    if (x == 10) {
        document.write("Hello"); // Bad practice
    }
}

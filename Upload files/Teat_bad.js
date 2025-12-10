// Hardcoded API token
const TOKEN = "abcd1234-SECRET-TOKEN";

function insecureLogin(username, password) {
    // DOM XSS
    document.body.innerHTML = "<h1>Welcome " + username + "</h1>";

    // Eval injection
    eval("console.log('User logged: " + username + "')");

    // SQL injection
    let query = "SELECT * FROM users WHERE name = '" + username + "'";
    console.log("Query:", query);

    // Callback hell + bad async
    setTimeout(() => {
        fetch("/api/user/" + username)
            .then(r => r.json())
            .then(d => {
                setTimeout(() => {
                    console.log("User:", d);
                }, 1000);
            });
    }, 1000);
}

// Global variable leak
data = [];

function unsafeMerge(a, b) {
    return Object.assign(a, b); // prototype pollution possible
}

const express = require("express");
const bodyParser = require("body-parser");
const app = express();
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }));

app.post("/", (req, res) => {
    if (!req.body) {
        return res.status(400).send({ message: "Content can not be empty" });
    }
    if (!req.body.username) {
        return res.status(400).send({ message: "Username is required" });
    }
    if (!req.body.password) {
        return res.status(400).send({ message: "Password is required" });
    }

    if (req.body.username !== "admin" || req.body.password !== "admin") {
        return res.status(401).send({ message: "Invalid username or password" });
    }

    return res.status(200).send({ message: "Login success" });
});

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
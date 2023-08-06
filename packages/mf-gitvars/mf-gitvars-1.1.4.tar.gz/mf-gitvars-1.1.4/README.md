# GitVars
Use the Gitlab API to extract CI/CD variables and output them in a format useable for running projects locally.

### Setup
Create an API key on Gitlab [here](https://gitlab.com/-/profile/personal_access_tokens) and grant it `read_api, read_repository` permissions

Create a local configuration file
`cat ~/.python-gitlab.cfg`

```ini
[global]
default = momentfeed
ssl_verify = true
timeout = 5
api_version = 4

[momentfeed]
url = https://gitlab.com
private_token = token123
```

### Usage
Find the gitlab project id on the project page here:

![Gitlab Project Id](projectid.png)

And then run with 
```bash
$ mf-gitvars [project-id]
```

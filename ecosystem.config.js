module.exports = {
  apps : [
{
       	"name": "rob bot",
	"script": "/home/possessor/Projects/ROBBOT/main.py",
	"cwd" : "/home/possessor/Projects/ROBBOT/",
	"wait_ready": true,
	"autorestart": true,
	"max_restarts": 8,
	"interpreter" : "/home/possessor/Projects/ROBBOT/botvenv/bin/python3.10"
}
],

  deploy : {
    production : {
      user : 'SSH_USERNAME',
      host : 'SSH_HOSTMACHINE',
      ref  : 'origin/master',
      repo : 'GIT_REPOSITORY',
      path : 'DESTINATION_PATH',
      'pre-deploy-local': '',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};

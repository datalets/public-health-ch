Public Health Schweiz
=====================

Website of the [Swiss Society for Public Health](http://public-health.ch), developed by [datalets,ch](http://datalets.ch) using the open source, [Django](https://www.djangoproject.com/)-based [Wagtail CMS](http://wagtail.io). The frontend is implemented by [moving water](http://www.movingwater.ch/) using [Bootstrap](https://getbootstrap.com) framework.

This project is open source under the [MIT License](LICENSE.md).

[![Dependency Status](https://dependencyci.com/github/datalets/public-health-ch/badge)](https://dependencyci.com/github/datalets/public-health-ch)

## Development environment

The easiest way to set up your machine would be to use [Vagrant](https://vagrantup.com), then in the project folder in the terminal type: `vagrant up`. Then when it is ready, follow instructions for *publichealth/static/org/archive-message.html#Database setup*.

To set up a full development environment, follow all these instructions.

**Frontend setup**

Make sure a recent version of node.js (we recommend using [nave.sh](https://gipublichealth/static/org/archive-message.htmlthub.com/isaacs/nave)), then:

```
npm install -g yarn grunt-cli
yarn install
```

The first command (`..install -g..`) may require `sudo` if you installed node.js as a system package. Afterwards, to compile the frontend, you should be able to run:

`grunt`

If you are only working on the frontend, you can start a local webserver and work on frontend assets without the backend setup described below. There is a `grunt browser-sync` setup for working with frontend assets.

(In a Vagrant shell, use the alias `watch`)

**Backend setup**

If not using Vagrant: after installing Python 3, from the project folder, deploy system packages and create a virtual environment as detailed (for Ubuntu users) below:

```
sudo apt-get install python3-venv python3-dev libjpeg-dev

pyvenv env
. env/bin/activate

pip install -U pip
pip install -r requirements.txt
```

At this point your backup is ready to be deployed.

## Database setup

Once your installation is ready, you can get a blank database set up and add a user to login with.

If you are using Vagrant, enter the shell of your virtual machine now with `vagrant ssh`

Run these commands:

```
./manage.py migrate
./manage.py createsuperuser
```

You will be asked a few questions to create an administrator account.

**Starting up**

If you have one installed, also start your local redis server (`service redis start`).

After completing setup, you can use:

```
./manage.py runserver
```

(In a Vagrant shell, just use `djrun`)

Now access the admin panel with the user account you created earlier: http://localhost:8000/admin/

## Troubleshooting

- Issues with migrating database tables in SQLite during development? Try `./manage.py migrate --fake`

## Production notes

We use [Ansible](https://www.ansible.com) and [Docker Compose](https://docs.docker.com/compose/reference/overview/) for automated deployment.

To use Docker Compose to manually deploy the site, copy `ansible/roles/web/templates/docker-compose.j2` to `/docker-compose.yml` and fill in all `{{ variables }}`. This can also be done automatically in Ansible.

Install or update the following roles from [Ansible Galaxy](https://docs.ansible.com/ansible/latest/reference_appendices/galaxy.html) to use our scripts:

```
ansible-galaxy install \
   dev-sec.nginx-hardening \
   dev-sec.ssh-hardening \
   dev-sec.os-hardening \
   geerlingguy.nodejs
```

To check that the scripts and roles are correctly installed, use this command to do a "dry run":

```
ansible-playbook ansible/*.yaml -i ansible/inventories/production --list-tasks
```

If you only want to run a certain set of actions, subset the tags which you see in the output above. For example, to only update the NGINX configuration:

```
ansible-playbook ansible/web.yaml -i ansible/inventories/production --tags "nginx_template_config"
```

To do production deployments, you need to obtain SSH and vault keys from your system administrator (who has followed the Ansible guide to set up a vault..), and place these in a `.keys` folder. To deploy a site:

```
ansible-playbook ansible/*.yaml -i ansible/inventories/production
```

For an update release with a specific version (tag or branch), use (the `-v` parameter showing output of commands):

```
ansible-playbook ansible/site.yaml -i ansible/inventories/production --tags release -v -e gitversion=<v*.*.*>
```

You can also use the `gitrepo` parameter to use a different fork of the source code.

Once the basic system set up, i.e. you have an `ansible` user in the sudoers and docker group, you are ready to run the playbook.

The typical order of deployment is:

- internet.yaml
- docker.yaml
- node.yaml
- web.yaml
- wagtail.yaml

### Production releases

For further deployment and system maintenance we have a `Makefile` which automates Docker Compose tasks. This should be converted to use [Ansible Container](http://docs.ansible.com/ansible-container/getting_started.html). In the meantime, start a release with Ansible, then complete it using `make`, i.e.:

```
ansible-playbook -i ansible/inventories/production --tags release ansible/wagtail.yaml
ssh -i .keys/ansible.pem ansible@<server-ip> "cd <release_dir> && make release"
```

This is already part of the normal release cycle, but if you wish to update the Docker images to the latest versions separately, use:

`make upgrade`

### Restoring a data backup

For development, it's handy to have access to a copy of the production data. To delete your local database and restore from a file backup, run:

```
rm publichealth-dev.sqlite3
python manage.py migrate
python manage.py loaddata publichealth.home.json
```

You might want to `createsuperuser` again at this point.

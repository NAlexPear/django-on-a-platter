# django-on-a-platter

Example repo to spike using a branchable Platter Postgres database (<https://platter.dev>) to back a
Django application.

## Setup for development

This repo is a spike, e.g. it commits it's production secret to GitHub, so don't deploy it directly
😅. All the branching functionality hacked into this repo will be nicely wrapped up in `platter` and
its generated code in the future.

- Install `pipenv`
- Install deps with `pipenv install`
- Install `platter` somewhere on your PATH, ensuring you have an account from
  <https://dashboard.platter.dev/register>
- Log in to your Platter account: `platter identity login`
- Launch a project-specific shell: `pipenv shell`

### Troubleshooting dev setup

- psychopg2 will not install cleanly: this can be a finicky package. On Mac, for instance, you may
  have to explicitly install and/or add openssl libs to the library path, e.g.:

    ```bash
    brew install openssl
    LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/ pipenv install psycopg2
    ```

## Develop

- Ensure you have a Platter database instance name: `platter postgres create <instance_name>`. This
  command will ask you to pick platforms; choose none, and then pick the default path. No code will
  be generated, but your database will be created. In the future `platter postgres create` will be
  less tied to node/web installations.
- Run `./platter_watch <instance_name>`, which will track the current git branch and configure the
  Django app to use the appropriate Platter database branch (read more about Platter resource
  branching [here](https://docs.platter.dev/concepts/branching)).
- In another terminal/tab, run the Django app: `python manage.py runserver`
- Now, as long as those two processes are running, whenever you check out a new branch,
  `platter_watch` will create config that your app can use to connect to a database branch, and your
  dev server will automatically reload.

## Deploy

Hey, this is just a spike! But if you really want to deploy it, you should just run `python
testsite/update_db.py <instance_name> master` before running migrations and starting the server in
your deployment.

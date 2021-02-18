from os.path import dirname, join, realpath
import re
import subprocess
from operator import itemgetter


POSTGRES_HOST_STRING_REGEXP = re.compile('''
  ^
  postgres://
  (?P<USER>[^:]+)
  :
  (?P<PASSWORD>[^@]+)
  @
  (?P<HOST>[^:]+)
  :
  (?P<PORT>\d+)
  /
  (?P<NAME>.+)
  $
''', re.VERBOSE)


def get_platter_db(instance, branch):
    platter_process = subprocess.Popen(
        [
            'platter',
            'postgres',
            'branch',
            'url',
            branch,
            '--instance',
            instance,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    host_string, err = platter_process.communicate()
    if err:
        return None, err
    m = re.match(
        POSTGRES_HOST_STRING_REGEXP,
        host_string.decode("utf-8").strip()
    )
    return m.groupdict(), None


def create_platter_db(instance, branch):
    platter_process = subprocess.Popen(
        [
            'platter',
            'postgres',
            'branch',
            'create',
            branch,
            '--instance',
            instance,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return platter_process.communicate()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print('Usage: {} <instance> <branch>'.format(sys.argv[0]))
        sys.exit()

    _, instance, branch = sys.argv
    print('Updating database connection for Django')
    _db_dict, err = get_platter_db(instance, branch)
    if err:
        print('DB branch {} not found; creating it now'.format(branch))
        success, err2 = create_platter_db(instance, branch)
        print('Branch {} created'.format(branch))
        if err2:
            print('Error fetching or creating Platter DB config:\n\n{}\n{}'.format(
                err.decode("utf-8"),
                err2.decode("utf-8")))
            sys.exit(1)
        print('Getting DB configuration for new branch {}'.format(branch))
        _db_dict, _ = get_platter_db(instance, branch)

    print('Writing DB configuration for branch {}'.format(branch))
    db_path = dirname(realpath(__file__))
    with open(join(db_path, 'db.py'), 'w') as file:
        # janky, but we write as a python dict to take easy advantage of Django's
        # standard dev server reloading and an easy dictionary merge in settings.py
        file.write("platter_db = {}".format(str(_db_dict)))

    print('\N{grinning face} Done configuring database connection for {}:{}!'.format(
        instance, branch))

import logging
import os
import re
import sys

from .constants import *
from .args import parse_arguments, get_version


def print_python_path():
    logging.debug('Current PYTHONPATH:')
    for p in sys.path:
        logging.debug(f'\t{p}')


def print_server_info():
    print()
    print(f"Azure ML Inferencing HTTP server v{get_version()}")
    print()


def print_cli_args(args):
    print()
    print("Server Settings")
    print("---------------")
    for arg in args.__dict__:
        print(arg + ": " + str(args.__dict__[arg]))
    print()


def print_routes(args):
    print()
    print("Server Routes")
    print("---------------")
    print(f"Liveness Probe: GET   127.0.0.1:{args.port}/")
    print(f"Score:          POST  127.0.0.1:{args.port}/score")
    print()


def set_environment_variables(args):
    os.environ[ENV_AML_APP_ROOT] = os.path.dirname(
        os.path.realpath(args.entry_script))
    os.environ[ENV_AZUREML_ENTRY_SCRIPT] = os.path.basename(
        os.path.realpath(args.entry_script))
    if args.model_dir is not None:
        os.environ[ENV_AZUREML_MODEL_DIR] = args.model_dir
    elif ENV_AZUREML_MODEL_DIR not in os.environ:
        print(f"The environment variable '{ENV_AZUREML_MODEL_DIR}' has not been set.")
        print("Use the --model_dir command line argument to set it.")

    os.environ[ENV_AML_APP_INSIGHTS_ENABLED] = "false"
    if args.appinsights_instrumentation_key is not None:
        uuid4hex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z', re.I)
        result = re.match(uuid4hex, args.appinsights_instrumentation_key)
        if result:
            os.environ[ENV_AML_APP_INSIGHTS_ENABLED] = "true"
            os.environ[ENV_AML_APP_INSIGHTS_KEY] = args.appinsights_instrumentation_key
        else:
            print(
                f"Invalid Application Insights instrumentation key provided: '{args.appinsights_instrumentation_key}'.")
            print("Application Insights has been disabled.")


def set_path_variable(args):
    sys.path.append(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'server'))
    sys.path.append(os.path.dirname(os.path.realpath(args.entry_script)))


def run():
    args = parse_arguments()

    set_environment_variables(args)
    set_path_variable(args)

    print_server_info()
    print_cli_args(args)
    print_routes(args)
    print_python_path()

    if sys.platform == 'win32':
        from azureml_inference_server_http import amlserver_win as srv
    else:
        from azureml_inference_server_http import amlserver_linux as srv

    srv.run(DEFAULT_HOST, args.port, args.worker_count)


if __name__ == "__main__":
    run()

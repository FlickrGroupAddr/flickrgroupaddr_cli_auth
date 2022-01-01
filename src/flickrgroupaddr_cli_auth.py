import argparse
import flickrapi
import json

def _get_api_keys( args ):
    with open( args.api_key_json, "r" ) as api_key_handle:
        api_key_info = json.load( api_key_handle )

    return api_key_info


def _read_args():
    arg_parser = argparse.ArgumentParser(description="FlickrGroupAddr CLI tool to get API key")
    arg_parser.add_argument( "api_key_json", help="JSON file with API key and secret" )

    return arg_parser.parse_args()

def _main():
    args = _read_args()
    api_key_info = _get_api_keys( )



if __name__ == "__main__":
    _main()


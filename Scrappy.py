import requests
import json
from bs4 import BeautifulSoup
import bs4
import argparse


def get_config(file_name):
    try:
        return json.load(open(file_name))
    except ValueError:
        print("not valid json")
        return None
    except FileNotFoundError:
        print("File not found")
        return None


def get_soup_from_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def get_element(soup, config):

    elements = None

    if "property" not in config.keys():
        elements = soup.find_all(config["tag"])

    if "property" in config.keys() and config["property"] == "class":
        elements = soup.find_all(class_=config["value"])
    if "property" in config.keys() and config["property"] == "id":
        elements = soup.find_all(id=config["value"])

    if "index" in config.keys():
        if config["index"] <= len(elements):
            elements = elements[config["index"] - 1]
        else:
            print("Index not found")

    return elements


def get_data_from_element(soups, config):

    def get_data(soup):
        if "prop" in config.keys():
            return soup[config["prop"]]
        else:
            return soup.text

    if isinstance(soups, bs4.element.ResultSet):
        res = []
        for soup in soups:
            res.append(get_data(soup))
        return res
    elif isinstance(soups, bs4.element.Tag):
        return get_data(soups)


def get_data_from_config(soup, config):
    components = get_element(soup, config["component"])
    elements = config["component"]["elements"]

    res_dict = {}
    res_list = []

    def get_data_from_component(com, elems):
        for elem in elems:
            if "component" in elem.keys():
                res_dict.update({elem["name"]: get_data_from_config(com, elem)})
            else:
                res_dict.update({elem["name"]: get_data_from_element(get_element(com, elem), elem)})
                res_list.append(res_dict)

    if isinstance(components, bs4.element.ResultSet):
        for component in components:
            get_data_from_component(component, elements)

    if isinstance(components, bs4.element.Tag):
        get_data_from_component(components, elements)

    if res_list:
        return res_list
    else:
        return res_dict


def scrap_from_config_file(file_name):
    return scrap(get_config(file_name))


def scrap(config):

    if not config:
        print("config is empty")
        return

    base_url = config["base_url"]

    keys = list(config)
    keys.remove("base_url")

    res = []

    for key in keys:
        soup = get_soup_from_url(base_url+config[key]["path"])
        data = get_data_from_config(soup, config[key])
        res.append({key: data})

    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--file', dest="file_name", action="store",
                        help='file location of the config', required=True)
    args = parser.parse_args()
    print(scrap_from_config_file(args.file_name))

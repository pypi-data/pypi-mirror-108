# -*- coding: utf-8 -*-

__license__ = "MIT"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"


import os
import argparse
import subprocess
import yaml
import csv


class WeCoded():

    def __init__(self, args):
        self.args = args
        self.config = None
        self.all_stats = dict()
        self.found_authors = set()

    def __load_config(self):
        with open(self.args["config_file"], 'r') as YAMLFile:
            self.config = yaml.load(YAMLFile, Loader=yaml.FullLoader)

    def __get_author_name(self, author):
        if "authors" in self.config:
            for n in self.config["authors"]:
                if author in n["aliases"]:
                    return n["name"]
        return author

    def run(self):
        os.makedirs(self.args["workpath"], exist_ok=True)
        self.__load_config()
        if not self.args["no_clone"]:
            self.__clone_repositories()
        if not self.args["no_stats"]:
            self.__compute_stats()
            self.__write_stats()

    def __clone_repositories(self):
        for r in self.config["repositories"]:
            print("### Cloning", r["name"], "####################")
            cmd = ["git", "clone", r["url"]]
            if "revision" in r:
                cmd.extend(["-b", r["revision"]])
            cmd.append(r["name"])
            subprocess.run(cmd, cwd=self.args["workpath"])

    def __compute_stats(self):
        for r in self.config["repositories"]:
            print("### Computing stats for", r["name"], "####################")
            cmd = ["git", "summary", "--line"]
            ret = subprocess.run(cmd, cwd=os.path.join(self.args["workpath"], r["name"]), capture_output=True)
            output = ret.stdout.decode("utf-8")
            lines = output.split("\n")
            stats = dict()
            lines = [x for x in lines if x]  # remove empty lines
            for line in lines:
                if ':' not in line:
                    data = [x for x in line.split(' ') if x]
                    data = data[:-1]  # remove latest field (percentage)
                    count = int(data[0])
                    author = " ".join(data[1:])  # join all fields fbut first for author name
                    author = self.__get_author_name(author)
                    if author not in stats:
                        stats[author] = 0
                    stats[author] += count
                    self.found_authors.add(author)
            self.all_stats[r["name"]] = stats

    def __write_stats(self):
        with open(os.path.join(self.args["workpath"], "stats.csv"), 'w', newline='') as csvfile:
            fields = list()
            fields.append('author')
            default_row = {'author': ''}
            for r in self.config["repositories"]:
                fields.append(r["name"])
                default_row[r["name"]] = 0
            writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=';')
            writer.writeheader()
            for a in self.found_authors:
                row = default_row.copy()
                row['author'] = a
                for r in self.config["repositories"]:
                    repos = r["name"]
                    if a in self.all_stats[repos].keys():
                        row[repos] = self.all_stats[repos][a]
                writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description=("A tool for contributions stats by authors "
                                                  "on multiple git repositories"))
    parser.add_argument("workpath", type=str,
                        help="the work path")
    parser.add_argument("-f", "--config-file", type=str, default=os.path.join(os.getcwd(), "wecoded-config.yaml"),
                        help='the path to the YAML configuration file (default: %(default)s)')
    parser.add_argument("-c", "--no-clone", action="store_true", default=False,
                        help="disable the cloning of remote repositories")
    parser.add_argument("-s", "--no-stats", action="store_true", default=False,
                        help="disable the computation of stats")

    args = vars(parser.parse_args())

    wc = WeCoded(args)
    wc.run()

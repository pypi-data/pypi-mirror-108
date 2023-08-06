import configparser
import os
import requests


class HCMConfigParser:
    def __init__(self, config_path=None, command_line=None):
        self._conf_ = configparser.RawConfigParser()
        if config_path is not None:
            self.load_path(config_path)

        self.load_environ()

        if command_line is not None:
            self.load_string(command_line)

    def load_path(self, config_path) -> None:
        _config_d_path = os.path.join(config_path, 'conf.d')
        if os.path.exists(_config_d_path):
            for _conf in os.listdir(_config_d_path):
                _conf = os.path.join(_config_d_path, _conf)
                self.append_config(_conf)

        # 处理ConfigMap目录
        _config_map_path = os.path.join(config_path, 'conf.map')
        if os.path.isdir(_config_map_path):
            for _file_name in os.listdir(_config_map_path):
                _file = os.path.join(_config_map_path, _file_name)
                if os.path.isfile(_file):
                    with open(_file, 'r') as _f:
                        _file_name_split = _file_name.split(".")
                        if len(_file_name_split) > 1:
                            _section = _file_name_split[0]
                            _conf_name = _file_name_split[1]
                            _conf_value = ''.join([x for x in _f.read().split("\n") if not x.startswith("#")])
                            self.set_conf(_section, _conf_name, _conf_value)

    def load_environ(self) -> None:
        # 处理环境变量：环境变量直接进入配置，如 logger_root__level=INFO，则配置logger_root.level=INFO
        for _k, _v in list(os.environ.items()):
            _conf_split = _k.split("__")
            if len(_conf_split) > 1 and self.has_option(_conf_split[0], _conf_split[1]):
                self.set_conf(_conf_split[0], _conf_split[1], _v)

    def append_config(self, conf):
        _append = configparser.RawConfigParser()
        if conf.startswith("http://") or conf.startswith("https://"):
            res = requests.get(conf)
            _append.read_string(res.text)
        else:
            _append.read(conf, "utf-8")

        for sn in _append.sections():
            for attr in _append.options(sn):
                if sn not in self._conf_.sections():
                    self._conf_.add_section(sn)
                self._conf_.set(sn, attr, _append.get(sn, attr))

    def load_string(self, command_line):
        command_line = command_line if isinstance(command_line, list) else [command_line]
        for _cmd_line in command_line:
            if _cmd_line.startswith("--"):
                _cmd_line = _cmd_line[2:]
                _key, _value = _cmd_line.split("=")
                _sec, _sec_key = _key.split('.')
                self.set_conf(_sec, _sec_key, _value)

    def get_conf(self, _section, _key=None, conf_type=bytes, default=None):
        """
        读取配置
        :param _section:
        :param _key:
        :param conf_type:
        :param default:
        :return:
        """
        try:
            if _key is None:
                return self._conf_.items(_section)
            else:
                if bool == conf_type or conf_type == bool:
                    return self._conf_.getboolean(_section, _key)
                elif int == conf_type:
                    return int(self._conf_.get(_section, _key))
                else:
                    return self._conf_.get(_section, _key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set_conf(self, _section, _key, _value):
        """
        设置配置
        :param _section:
        :param _key:
        :param _value:
        :return:
        """
        if _section not in self._conf_.sections():
            self._conf_.add_section(_section)
        self._conf_.set(_section, _key, _value)

    def has_option(self, _section, _option):
        return _section in self._conf_.sections() and _option in self._conf_.options(_section)

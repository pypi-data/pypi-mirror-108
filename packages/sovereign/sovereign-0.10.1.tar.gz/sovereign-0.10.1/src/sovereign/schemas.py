import zlib
import warnings
import multiprocessing
from collections import defaultdict
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field, BaseSettings, SecretStr, validator
from typing import List, Any, Dict, Union, Optional, Tuple, Sized, Type
from jinja2 import meta, Template
from fastapi.responses import JSONResponse
from sovereign.config_loader import jinja_env, Serialization, Protocol, Loadable
from sovereign.utils.version_info import compute_hash


JsonResponseClass: Type[JSONResponse] = JSONResponse
# pylint: disable=unused-import
try:
    import orjson
    from fastapi.responses import ORJSONResponse

    JsonResponseClass = ORJSONResponse
except ImportError:
    try:
        import ujson
        from fastapi.responses import UJSONResponse

        JsonResponseClass = UJSONResponse
    except ImportError:
        pass


class CacheStrategy(str, Enum):
    context = "context"
    content = "content"


class SourceData(BaseModel):
    scopes: Dict[str, List[Dict[str, Any]]] = defaultdict(list)


class ConfiguredSource(BaseModel):
    type: str
    config: Dict[str, Any]
    scope: str = "default"  # backward compatibility


class SourceMetadata(BaseModel):
    updated: datetime = datetime.fromtimestamp(0)
    count: int = 0

    def update_date(self) -> None:
        self.updated = datetime.now()

    def update_count(self, iterable: Sized) -> None:
        self.count = len(iterable)

    @property
    def is_stale(self) -> bool:
        return self.updated < (datetime.now() - timedelta(minutes=2))

    def __str__(self) -> str:
        return (
            f"Sources were last updated at {datetime.isoformat(self.updated)}. "
            f"There are {self.count} instances."
        )


class StatsdConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8125
    tags: Dict[str, Union[Loadable, str]] = dict()
    namespace: str = "sovereign"
    enabled: bool = False
    use_ms: bool = True

    @validator("tags", pre=True)
    def load_tags(cls, v: Dict[str, Union[Loadable, str]]) -> Dict[str, Any]:
        ret = dict()
        for key, value in v.items():
            if isinstance(value, dict):
                ret[key] = Loadable(**value).load()
            elif isinstance(value, str):
                ret[key] = Loadable.from_legacy_fmt(value).load()
            else:
                raise ValueError(f"Received an invalid tag for statsd: {value}")
        return ret


class XdsTemplate:
    def __init__(self, path: Union[str, Loadable]) -> None:
        if isinstance(path, str):
            self.loadable: Loadable = Loadable.from_legacy_fmt(path)
        elif isinstance(path, Loadable):
            self.loadable = path
        self.is_python_source = self.loadable.protocol == Protocol.python
        self.source = self.load_source()
        self.checksum = zlib.adler32(self.source.encode())

    async def __call__(self, *args: Any, **kwargs: Any) -> Union[Dict[str, Any], str]:
        if self.is_python_source:
            code = self.loadable.load()
            try:
                return {"resources": list(code.call(*args, **kwargs))}
            except TypeError as e:
                message_start = str(e).find(":")
                missing_args = str(e)[message_start + 2 :]
                supplied_args = list(kwargs.keys())
                raise TypeError(
                    f"Tried to render a template using partial arguments. "
                    f"Missing args: {missing_args}. Supplied args: {args} "
                    f"Supplied keyword args: {supplied_args}"
                )
        else:
            content: Template = self.loadable.load()
            return await content.render_async(*args, **kwargs)

    def jinja_variables(self) -> List[str]:
        template_ast = jinja_env.parse(self.source)
        return meta.find_undeclared_variables(template_ast)  # type: ignore

    def load_source(self) -> str:
        if self.loadable.serialization in (Serialization.jinja, Serialization.jinja2):
            # The Jinja2 template serializer does not properly set a name
            # for the loaded template.
            # The repr for the template prints out as the memory address
            # This makes it really hard to generate a consistent version_info string
            # in rendered configuration.
            # For this reason, we re-load the template as a string instead, and create a checksum.
            old_serialization = self.loadable.serialization
            self.loadable.serialization = Serialization("string")
            ret = self.loadable.load()
            self.loadable.serialization = old_serialization
            return str(ret)
        elif self.is_python_source:
            # If the template specified is a python source file,
            # we can simply read and return the source of it.
            old_protocol = self.loadable.protocol
            old_serialization = self.loadable.serialization
            self.loadable.protocol = Protocol("inline")
            self.loadable.serialization = Serialization("string")
            ret = self.loadable.load()
            self.loadable.protocol = old_protocol
            self.loadable.serialization = old_serialization
            return str(ret)
        else:
            # The only other supported serializers are string, yaml, and json
            # So it should be safe to create this checksum off
            return str(self.source)


class ProcessedTemplate:
    def __init__(
        self,
        resources: List[Dict[str, Any]],
        type_url: str,
        version_info: Optional[str],
    ) -> None:
        for resource in resources:
            if "@type" not in resource:
                resource["@type"] = type_url
        self.resources = resources
        self.version_info = version_info

    @property
    def version(self) -> str:
        return self.version_info or compute_hash(self.resources)

    @property
    def rendered(self) -> bytes:
        return JsonResponseClass().render(
            content={
                "version_info": self.version,
                "resources": self.resources,
            }
        )

    def deserialize_resources(self) -> List[Dict[str, Any]]:
        return self.resources


class ProcessedTemplates:
    def __init__(self, types: Optional[Dict[str, ProcessedTemplate]] = None) -> None:
        if types is None:
            self.types = dict()
        else:
            self.types = types


class Locality(BaseModel):
    region: str = Field(None)
    zone: str = Field(None)
    sub_zone: str = Field(None)


class SemanticVersion(BaseModel):
    major_number: int = 0
    minor_number: int = 0
    patch: int = 0

    def __str__(self) -> str:
        return f"{self.major_number}.{self.minor_number}.{self.patch}"


class BuildVersion(BaseModel):
    version: SemanticVersion = SemanticVersion()
    metadata: Dict[str, Any] = {}


class Extension(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    version: Optional[BuildVersion] = None
    disabled: Optional[bool] = None


class Node(BaseModel):
    id: str = Field("-", title="Hostname")
    cluster: str = Field(
        ...,
        title="Envoy service-cluster",
        description="The ``--service-cluster`` configured by the Envoy client",
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, title="Key:value metadata")
    locality: Locality = Field(Locality(), title="Locality")
    build_version: str = Field(
        None,  # Optional in the v3 Envoy API
        title="Envoy build/release version string",
        description="Used to identify what version of Envoy the "
        "client is running, and what config to provide in response",
    )
    user_agent_name: str = "envoy"
    user_agent_version: str = ""
    user_agent_build_version: BuildVersion = BuildVersion()
    extensions: List[Extension] = []
    client_features: List[str] = []

    @property
    def common(self) -> Tuple[str, str, str, BuildVersion, Locality]:
        """
        Returns fields that are the same in adjacent proxies
        ie. proxies that are part of the same logical group
        """
        return (
            self.cluster,
            self.build_version,
            self.user_agent_version,
            self.user_agent_build_version,
            self.locality,
        )


class Resources(List[str]):
    """
    Acts like a regular list except it returns True
    for all membership tests when empty.
    """

    def __contains__(self, item: object) -> bool:
        if len(self) == 0:
            return True
        return item in list(self)


class DiscoveryRequest(BaseModel):
    node: Node = Field(..., title="Node information about the envoy proxy")
    version_info: str = Field(
        "0", title="The version of the envoy clients current configuration"
    )
    resource_names: Resources = Field(
        Resources(), title="List of requested resource names"
    )
    hide_private_keys: bool = False
    type_url: str = Field(
        None, title="The corresponding type_url for the requested resource"
    )
    desired_controlplane: str = Field(
        None, title="The host header provided in the Discovery Request"
    )

    @property
    def envoy_version(self) -> str:
        try:
            version = str(self.node.user_agent_build_version.version)
            assert version != "0.0.0"
        except AssertionError:
            try:
                build_version = self.node.build_version
                _, version, *_ = build_version.split("/")
            except (AttributeError, ValueError):
                # TODO: log/metric this?
                return "default"
        return version

    @property
    def resources(self) -> Resources:
        return Resources(self.resource_names)

    @property
    def uid(self) -> str:
        return compute_hash(
            self.resources,
            self.node.common,
            self.desired_controlplane,
        )


class DiscoveryResponse(BaseModel):
    version_info: str = Field(
        ..., title="The version of the configuration in the response"
    )
    resources: List[Any] = Field(..., title="The requested configuration resources")


class SovereignAsgiConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8080
    keepalive: int = 5
    workers: int = multiprocessing.cpu_count() * 2 + 1
    reuse_port: bool = True
    log_level: str = "warning"
    worker_class: str = "uvicorn.workers.UvicornWorker"

    class Config:
        fields = {
            "host": {"env": "SOVEREIGN_HOST"},
            "port": {"env": "SOVEREIGN_PORT"},
            "keepalive": {"env": "SOVEREIGN_KEEPALIVE"},
            "workers": {"env": "SOVEREIGN_WORKERS"},
        }

    def as_gunicorn_conf(self) -> Dict[str, Any]:
        return {
            "bind": ":".join(map(str, [self.host, self.port])),
            "keepalive": self.keepalive,
            "reuse_port": self.reuse_port,
            "loglevel": self.log_level,
            "workers": self.workers,
            "worker_class": self.worker_class,
        }


class SovereignConfig(BaseSettings):
    sources: List[ConfiguredSource]
    templates: Dict[str, Dict[str, Union[str, Loadable]]]
    template_context: Dict[str, Any] = {}
    eds_priority_matrix: Dict[str, Dict[str, str]] = {}
    modifiers: List[str] = []
    global_modifiers: List[str] = []
    regions: List[str] = []
    statsd: StatsdConfig = StatsdConfig()
    auth_enabled: bool = False
    auth_passwords: str = ""
    encryption_key: str = ""
    environment: str = "local"
    debug_enabled: bool = False
    sentry_dsn: str = ""
    node_match_key: str = "cluster"
    node_matching: bool = True
    source_match_key: str = "service_clusters"
    sources_refresh_rate: int = 30
    cache_strategy: str = "context"
    refresh_context: bool = False
    context_refresh_rate: int = 3600
    dns_hard_fail: bool = False
    enable_application_logs: bool = False
    enable_access_logs: bool = True
    log_fmt: Optional[str] = ""
    ignore_empty_log_fields: bool = False

    class Config:
        fields = {
            "auth_enabled": {"env": "SOVEREIGN_AUTH_ENABLED"},
            "auth_passwords": {"env": "SOVEREIGN_AUTH_PASSWORDS"},
            "encryption_key": {"env": "SOVEREIGN_ENCRYPTION_KEY"},
            "environment": {"env": "SOVEREIGN_ENVIRONMENT"},
            "debug_enabled": {"env": "SOVEREIGN_DEBUG_ENABLED"},
            "sentry_dsn": {"env": "SOVEREIGN_SENTRY_DSN"},
            "node_match_key": {"env": "SOVEREIGN_NODE_MATCH_KEY"},
            "node_matching": {"env": "SOVEREIGN_NODE_MATCHING"},
            "source_match_key": {"env": "SOVEREIGN_SOURCE_MATCH_KEY"},
            "sources_refresh_rate": {"env": "SOVEREIGN_SOURCES_REFRESH_RATE"},
            "cache_strategy": {"env": "SOVEREIGN_CACHE_STRATEGY"},
            "refresh_context": {"env": "SOVEREIGN_REFRESH_CONTEXT"},
            "context_refresh_rate": {"env": "SOVEREIGN_CONTEXT_REFRESH_RATE"},
            "dns_hard_fail": {"env": "SOVEREIGN_DNS_HARD_FAIL"},
            "enable_application_logs": {"env": "SOVEREIGN_ENABLE_APPLICATION_LOGS"},
            "enable_access_logs": {"env": "SOVEREIGN_ENABLE_ACCESS_LOGS"},
            "log_fmt": {"env": "SOVEREIGN_LOG_FORMAT"},
            "ignore_empty_fields": {"env": "SOVEREIGN_LOG_IGNORE_EMPTY"},
        }

    @property
    def passwords(self) -> List[str]:
        return self.auth_passwords.split(",") or []

    def xds_templates(self) -> Dict[str, Dict[str, XdsTemplate]]:
        ret: Dict[str, Dict[str, XdsTemplate]] = {
            "__any__": {}
        }  # Special key to hold templates from all versions
        for version, templates in self.templates.items():
            loaded_templates = {
                _type: XdsTemplate(path=path) for _type, path in templates.items()
            }
            ret[str(version)] = loaded_templates
            ret["__any__"].update(loaded_templates)
        return ret

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        kwargs = [f"{k}={v}" for k, v in self.show().items()]
        return f"SovereignConfig({kwargs})"

    def show(self) -> Dict[str, Any]:
        safe_items = dict()
        for key, value in self.__dict__.items():
            if key in ["auth_passwords", "encryption_key", "passwords", "sentry_dsn"]:
                value = "redacted"
            safe_items[key] = value
        return safe_items


class TemplateSpecification(BaseModel):
    type: str
    spec: Loadable


class NodeMatching(BaseSettings):
    enabled: bool = True
    source_key: str = "service_clusters"
    node_key: str = "cluster"

    class Config:
        fields = {
            "enabled": {"env": "SOVEREIGN_NODE_MATCHING_ENABLED"},
            "source_key": {"env": "SOVEREIGN_SOURCE_MATCH_KEY"},
            "node_key": {"env": "SOVEREIGN_NODE_MATCH_KEY"},
        }


class AuthConfiguration(BaseSettings):
    enabled: bool = False
    auth_passwords: SecretStr = SecretStr("")
    encryption_key: SecretStr = SecretStr("")

    class Config:
        fields = {
            "enabled": {"env": "SOVEREIGN_AUTH_ENABLED"},
            "auth_passwords": {"env": "SOVEREIGN_AUTH_PASSWORDS"},
            "encryption_key": {"env": "SOVEREIGN_ENCRYPTION_KEY"},
        }


class ApplicationLogConfiguration(BaseSettings):
    enabled: bool = False
    # currently only support /dev/stdout as JSON

    class Config:
        fields = {
            "enabled": {"env": "SOVEREIGN_ENABLE_APPLICATION_LOGS"},
        }


class AccessLogConfiguration(BaseSettings):
    enabled: bool = True
    log_fmt: Optional[str] = None
    ignore_empty_fields: bool = False

    class Config:
        fields = {
            "enabled": {"env": "SOVEREIGN_ENABLE_ACCESS_LOGS"},
            "log_fmt": {"env": "SOVEREIGN_LOG_FORMAT"},
            "ignore_empty_fields": {"env": "SOVEREIGN_LOG_IGNORE_EMPTY"},
        }


class LoggingConfiguration(BaseSettings):
    application_logs: ApplicationLogConfiguration = ApplicationLogConfiguration()
    access_logs: AccessLogConfiguration = AccessLogConfiguration()


class ContextConfiguration(BaseSettings):
    context: Dict[str, Loadable] = {}
    refresh: bool = False
    refresh_rate: int = 3600

    @staticmethod
    def context_from_legacy(context: Dict[str, str]) -> Dict[str, Loadable]:
        ret = dict()
        for key, value in context.items():
            ret[key] = Loadable.from_legacy_fmt(value)
        return ret

    class Config:
        fields = {
            "refresh": {"env": "SOVEREIGN_REFRESH_CONTEXT"},
            "refresh_rate": {"env": "SOVEREIGN_CONTEXT_REFRESH_RATE"},
        }


class SourcesConfiguration(BaseSettings):
    refresh_rate: int = 30
    cache_strategy: CacheStrategy = CacheStrategy.context

    class Config:
        fields = {
            "refresh_rate": {"env": "SOVEREIGN_SOURCES_REFRESH_RATE"},
            "cache_strategy": {"env": "SOVEREIGN_CACHE_STRATEGY"},
        }


class LegacyConfig(BaseSettings):
    regions: Optional[List[str]] = None
    eds_priority_matrix: Optional[Dict[str, Dict[str, str]]] = None
    dns_hard_fail: Optional[bool] = None
    environment: Optional[str] = None

    @validator("regions")
    def regions_is_set(cls, v: Optional[List[str]]) -> List[str]:
        if v is not None:
            warnings.warn(
                "Setting regions via config is deprecated. "
                "It is suggested to use a modifier or template "
                "logic in order to achieve the same goal.",
                DeprecationWarning,
            )
            return v
        else:
            return []

    @validator("eds_priority_matrix")
    def eds_priority_matrix_is_set(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> Dict[str, Dict[str, Any]]:
        if v is not None:
            warnings.warn(
                "Setting eds_priority_matrix via config is deprecated. "
                "It is suggested to use a modifier or template "
                "logic in order to achieve the same goal.",
                DeprecationWarning,
            )
            return v
        else:
            return {}

    @validator("dns_hard_fail")
    def dns_hard_fail_is_set(cls, v: Optional[bool]) -> bool:
        if v is not None:
            warnings.warn(
                "Setting dns_hard_fail via config is deprecated. "
                "It is suggested to supply a module that can perform "
                "dns resolution to template_context, so that it can "
                "be used via templates instead.",
                DeprecationWarning,
            )
            return v
        else:
            return False

    @validator("environment")
    def environment_is_set(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            warnings.warn(
                "Setting environment via config is deprecated. "
                "It is suggested to configure this value through log_fmt "
                "instead.",
                DeprecationWarning,
            )
            return v
        else:
            return None

    class Config:
        fields = {
            "dns_hard_fail": {"env": "SOVEREIGN_DNS_HARD_FAIL"},
            "environment": {"env": "SOVEREIGN_ENVIRONMENT"},
        }


class SovereignConfigv2(BaseSettings):
    sources: List[ConfiguredSource]
    templates: Dict[str, List[TemplateSpecification]]
    source_config: SourcesConfiguration = SourcesConfiguration()
    modifiers: List[str] = []
    global_modifiers: List[str] = []
    template_context: ContextConfiguration = ContextConfiguration()
    matching: NodeMatching = NodeMatching()
    authentication: AuthConfiguration = AuthConfiguration()
    logging: LoggingConfiguration = LoggingConfiguration()
    statsd: StatsdConfig = StatsdConfig()
    sentry_dsn: SecretStr = SecretStr("")
    debug: bool = False
    legacy_fields: LegacyConfig = LegacyConfig()

    class Config:
        fields = {
            "sentry_dsn": {"env": "SOVEREIGN_SENTRY_DSN"},
            "debug": {"env": "SOVEREIGN_DEBUG"},
        }

    @property
    def passwords(self) -> List[str]:
        return self.authentication.auth_passwords.get_secret_value().split(",") or []

    def xds_templates(self) -> Dict[str, Dict[str, XdsTemplate]]:
        ret: Dict[str, Dict[str, XdsTemplate]] = {
            "__any__": {}
        }  # Special key to hold templates from all versions
        for version, template_specs in self.templates.items():
            loaded_templates = {
                template.type: XdsTemplate(path=template.spec)
                for template in template_specs
            }
            ret[str(version)] = loaded_templates
            ret["__any__"].update(loaded_templates)
        return ret

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"SovereignConfigv2({self.dict()})"

    def show(self) -> Dict[str, Any]:
        return self.dict()

    @staticmethod
    def from_legacy_config(other: SovereignConfig) -> "SovereignConfigv2":
        new_templates = dict()
        for version, templates in other.templates.items():
            specs = list()
            for type, path in templates.items():
                if isinstance(path, str):
                    specs.append(
                        TemplateSpecification(
                            type=type, spec=Loadable.from_legacy_fmt(path)
                        )
                    )
                else:
                    # Just in case? Although this shouldn't happen
                    specs.append(TemplateSpecification(type=type, spec=path))
            new_templates[str(version)] = specs

        return SovereignConfigv2(
            sources=other.sources,
            templates=new_templates,
            source_config=SourcesConfiguration(
                refresh_rate=other.sources_refresh_rate,
                cache_strategy=other.cache_strategy,
            ),
            modifiers=other.modifiers,
            global_modifiers=other.global_modifiers,
            template_context=ContextConfiguration(
                context=ContextConfiguration.context_from_legacy(
                    other.template_context
                ),
                refresh=other.refresh_context,
                refresh_rate=other.context_refresh_rate,
            ),
            matching=NodeMatching(
                enabled=other.node_matching,
                source_key=other.source_match_key,
                node_key=other.node_match_key,
            ),
            authentication=AuthConfiguration(
                enabled=other.auth_enabled,
                auth_passwords=SecretStr(other.auth_passwords),
                encryption_key=SecretStr(other.encryption_key),
            ),
            logging=LoggingConfiguration(
                application_logs=ApplicationLogConfiguration(
                    enabled=other.enable_application_logs,
                ),
                access_logs=AccessLogConfiguration(
                    enabled=other.enable_access_logs,
                    log_fmt=other.log_fmt,
                    ignore_empty_fields=other.ignore_empty_log_fields,
                ),
            ),
            statsd=other.statsd,
            sentry_dsn=SecretStr(other.sentry_dsn),
            debug=other.debug_enabled,
            legacy_fields=LegacyConfig(
                regions=other.regions,
                eds_priority_matrix=other.eds_priority_matrix,
                dns_hard_fail=other.dns_hard_fail,
                environment=other.environment,
            ),
        )

from typing import List, Dict

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_resources.azure_resource_group import AzureResourceGroup
from cloudrail.knowledge.context.azure.azure_resources.web_app.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.azure_resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.azure_resources.web_app.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.environment_context import CheckovResult


class AzureEnvironmentContext(BaseEnvironmentContext):

    def __init__(self,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 resource_groups: AliasesDict[AzureResourceGroup] = None,
                 sql_servers: AliasesDict[AzureSqlServer] = None,
                 app_services: AliasesDict[AzureAppService] = None,
                 function_apps: AliasesDict[AzureFunctionApp] = None):
        BaseEnvironmentContext.__init__(self)
        self.checkov_results: Dict[str, List[CheckovResult]] = checkov_results or {}
        self.resource_groups: AliasesDict[AzureResourceGroup] = resource_groups or AliasesDict()
        self.sql_servers: AliasesDict[AzureSqlServer] = sql_servers or AliasesDict()
        self.app_services: AliasesDict[AzureAppService] = app_services or AliasesDict()
        self.function_apps: AliasesDict[AzureFunctionApp] = function_apps or AliasesDict()

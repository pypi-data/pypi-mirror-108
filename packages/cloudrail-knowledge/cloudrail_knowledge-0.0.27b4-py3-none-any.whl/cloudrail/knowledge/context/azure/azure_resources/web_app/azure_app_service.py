from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.azure_resources.web_app.site_config import SiteConfig


class AzureAppService(AzureResource):

    def __init__(self, subscription_id: str, resource_group_name: str, location: str, name: str,
                 app_service_plan_id: str, site_config: SiteConfig = None) -> None:
        super().__init__(subscription_id, resource_group_name, location,
                         'Microsoft.Web', AzureResourceType.AZURERM_APP_SERVICE)
        self.name = name
        self.app_service_plan_id: str = app_service_plan_id
        self.site_config: SiteConfig = site_config
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False

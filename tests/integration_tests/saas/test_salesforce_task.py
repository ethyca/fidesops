import pytest
import random
from requests import Response
from starlette.status import HTTP_200_OK

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors.saas_connector import SaaSConnector
from fidesops.task import graph_task
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration_saas
@pytest.mark.integration_salesforce
def test_salesforce_access_request_task(
    db,
    policy,
    salesforce_identity_email,
    salesforce_secrets,
    salesforce_connection_config,
    salesforce_dataset_config,
    salesforce_data
) -> None:
    """Test getting a contact (placeholder)
    """
    connector = SaaSConnector(salesforce_connection_config)
    headers = {
        "Authorization": f"Bearer {salesforce_secrets['access_token']}",
    }
    get_contact_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.GET,
        path=f"/services/data/v54.0/sobjects/Contact/Email/{salesforce_identity_email}",
        headers=headers,
    )
    get_contact_response: Response = connector.create_client().send(get_contact_request)
    assert HTTP_200_OK == get_contact_response.status_code
    
    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": salesforce_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = salesforce_connection_config.get_saas_config().fides_key
    merged_graph = salesforce_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    # import pdb;
    # pdb.set_trace()
        
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [salesforce_connection_config],
        {"email": salesforce_identity_email},
    )
    
    assert_rows_match(
        v[f"{dataset_name}:contact"],
        min_size=1,
        keys=[
            "attributes",
            "Id",
            "IsDeleted",
            "MasterRecordId",
            "AccountId",
            "LastName",
            "FirstName",
            "Salutation",
            "Name",
            "OtherStreet",
            "OtherCity",
            "OtherState",
            "OtherPostalCode",
            "OtherCountry",
            "OtherLatitude",
            "OtherLongitude",
            "OtherGeocodeAccuracy",
            "OtherAddress",
            "MailingStreet",
            "MailingCity",
            "MailingState",
            "MailingPostalCode",
            "MailingCountry",
            "MailingLatitude",
            "MailingLongitude",
            "MailingGeocodeAccuracy",
            "MailingAddress",
            "Phone",
            "Fax",
            "MobilePhone",
            "HomePhone",
            "OtherPhone",
            "AssistantPhone",
            "ReportsToId",
            "Email",
            "Title",
            "Department",
            "AssistantName",
            "LeadSource",
            "Birthdate",
            "Description",
            "OwnerId",
            "CreatedDate",
            "CreatedById",
            "LastModifiedDate",
            "LastModifiedById",
            "SystemModstamp",
            "LastActivityDate",
            "LastCURequestDate",
            "LastCUUpdateDate",
            "LastViewedDate",
            "LastReferencedDate",
            "EmailBouncedReason",
            "EmailBouncedDate",
            "IsEmailBounced",
            "PhotoUrl",
            "Jigsaw",
            "JigsawContactId",
            "CleanStatus",
            "IndividualId",
        ],
    )
    
    assert_rows_match(
        v[f"{dataset_name}:case"],
        min_size=1,
        keys=[
            "attributes",
            "Id",
            "IsDeleted",
            "MasterRecordId",
            "CaseNumber",
            "ContactId",
            "AccountId",
            "AssetId",
            "SourceId",
            "ParentId",
            "SuppliedName",
            "SuppliedEmail",
            "SuppliedPhone",
            "SuppliedCompany",
            "Type",
            "Status",
            "Reason",
            "Origin",
            "Subject",
            "Priority",
            "Description",
            "IsClosed",
            "ClosedDate",
            "IsEscalated",
            "OwnerId",
            "CreatedDate",
            "CreatedById",
            "LastModifiedDate",
            "LastModifiedById",
            "SystemModstamp",
            "ContactPhone",
            "ContactMobile",
            "ContactEmail",
            "ContactFax",
            "Comments",
            "LastViewedDate",
            "LastReferencedDate",
        ]
    )
    
    assert_rows_match(
        v[f"{dataset_name}:campaign_member"],
        min_size=1,
        keys=[
            "attributes",
            "Id",
            "IsDeleted",
            "CampaignId",
            "LeadId",
            "ContactId",
            "Status",
            "HasResponded",
            "CreatedDate",
            "CreatedById",
            "LastModifiedDate",
            "LastModifiedById",
            "SystemModstamp",
            "FirstRespondedDate",
            "Salutation",
            "Name",
            "FirstName",
            "LastName",
            "Title",
            "Street",
            "City",
            "State",
            "PostalCode",
            "Country",
            "Email",
            "Phone",
            "Fax",
            "MobilePhone",
            "Description",
            "DoNotCall",
            "HasOptedOutOfEmail",
            "HasOptedOutOfFax",
            "LeadSource",
            "CompanyOrAccount",
            "Type",
            "LeadOrContactId",
            "LeadOrContactOwnerId",
        ]
    )
    
    assert_rows_match(
        v[f"{dataset_name}:lead"],
        min_size=1,
        keys=[
            "attributes",
            "Id",
            "IsDeleted",
            "MasterRecordId",
            "LastName",
            "FirstName",
            "Salutation",
            "Name",
            "Title",
            "Company",
            "Street",
            "City",
            "State",
            "PostalCode",
            "Country",
            "Latitude",
            "Longitude",
            "GeocodeAccuracy",
            "Address",
            "Phone",
            "MobilePhone",
            "Fax",
            "Email",
            "Website",
            "PhotoUrl",
            "Description",
            "LeadSource",
            "Status",
            "Industry",
            "Rating",
            "AnnualRevenue",
            "NumberOfEmployees",
            "OwnerId",
            "IsConverted",
            "ConvertedDate",
            "ConvertedAccountId",
            "ConvertedContactId",
            "ConvertedOpportunityId",
            "IsUnreadByOwner",
            "CreatedDate",
            "CreatedById",
            "LastModifiedDate",
            "LastModifiedById",
            "SystemModstamp",
            "LastActivityDate",
            "LastViewedDate",
            "LastReferencedDate",
            "Jigsaw",
            "JigsawContactId",
            "CleanStatus",
            "CompanyDunsNumber",
            "DandbCompanyId",
            "EmailBouncedReason",
            "EmailBouncedDate",
            "IndividualId",
        ]
    )

    assert_rows_match(
        v[f"{dataset_name}:account"],
        min_size=1,
        keys=[
                        "attributes"
            "Id",
            "IsDeleted",
            "MasterRecordId",
            "Name",
            "Type",
            "ParentId",
            "BillingStreet",
            "BillingCity",
            "BillingState",
            "BillingPostalCode",
            "BillingCountry",
            "BillingLatitude",
            "BillingLongitude",
            "BillingGeocodeAccuracy",
            "BillingAddress",
            "ShippingStreet",
            "ShippingCity",
            "ShippingState",
            "ShippingPostalCode",
            "ShippingCountry",
            "ShippingLatitude",
            "ShippingLongitude",
            "ShippingGeocodeAccuracy",
            "ShippingAddress",
            "Phone",
            "Fax",
            "AccountNumber",
            "Website",
            "PhotoUrl",
            "Sic",
            "Industry",
            "AnnualRevenue",
            "NumberOfEmployees",
            "Ownership",
            "TickerSymbol",
            "Description",
            "Rating",
            "Site",
            "OwnerId",
            "CreatedDate",
            "CreatedById",
            "LastModifiedDate",
            "LastModifiedById",
            "SystemModstamp",
            "LastActivityDate",
            "LastViewedDate",
            "LastReferencedDate",
            "Jigsaw",
            "JigsawCompanyId",
            "CleanStatus",
            "AccountSource",
            "DunsNumber",
            "Tradestyle",
            "NaicsCode",
            "NaicsDesc",
            "YearStarted",
            "SicDesc",
            "DandbCompanyId",
            "OperatingHoursId",
        ]
    )
    
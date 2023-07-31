import boto3

def main():
    next_token = None
    next_token_quotas = None
    keywords = ['EC2', 'Elastic'] # Your keywords.

    # AWS Configure.
    session = boto3.Session(
        profile_name = '',
        region_name = ''
    )

    quotas_connection = session.client('service-quotas')

    while True:
        if next_token:
            response = quotas_connection.list_services(
                NextToken = next_token
            )
        else:
            response = quotas_connection.list_services()

        services = response['Services']

        try:
            next_token = response['NextToken']
        except:
            next_token = None

        for service in services:
            # Debug progress
            # print('.')

            service_code = service['ServiceCode']

            while True:
                if next_token_quotas:
                    service_quotas = quotas_connection.list_service_quotas(
                        ServiceCode = service_code,
                        NextToken = next_token_quotas
                    )
                else:
                    service_quotas = quotas_connection.list_service_quotas(
                        ServiceCode = service_code
                    )

                try:
                    next_token_quotas = service_quotas['NextToken']
                except:
                    next_token_quotas = None

                quotas_list = service_quotas['Quotas']

                for quota_service in quotas_list:                                     
                    quota_name = quota_service['QuotaName'].lower()

                    # print by quota name.
                    if any(word.lower() in quota_name for word in keywords):
                        print(f"{service['ServiceName']} -> {quota_service['QuotaName']} -> Value: {quota_service['Value']}")

                    # print by quota value(count).
                    # if quota_service['Value'] == 100 and quota_service['Adjustable']:
                    #     print(f"{quota_service['QuotaName']} -> {service['ServiceName']}")

                if not next_token_quotas:
                    break

        if not next_token:
            break

if __name__ == '__main__':
    print('Begin.')
    main()
    print('End.')
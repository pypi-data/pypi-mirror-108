
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json

class ElastalertWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        try:
            # Default parameters
            print("payload: "+str(payload))
            resource = payload['kubernetes']['pod_name']
            environment = 'Production'
            res = payload['event']
            event = res['eventName']
            severity =res['severity'].lower()
            group ='Elastalert'
            text = res['message']
            tags = []
            attributes = {}
            createTime = payload['@timestamp']
            try:
                origin = res['resourceXpath']
            except Exception as e:
                print("origin not defined")
                origin = ' '
        except Exception as e:
            print("Error reading payload: "+str(e)) 

        return Alert(
            resource = resource,
            event = event,
            severity = severity,
            service = ['example.com'],
            group = group,
            text = text,
            tags = tags,
            origin = origin,
            createTime = createTime,
            attributes = attributes,
            environment = environment
        #     environment=payload.get('environment', environment),
        #     severity=payload.get('severity', severity),
        #     service=['fail2ban'],
        #     group=payload.get('group', group),
        #     value='BAN',
        #     text=payload.get('message', text),
        #     tags=payload.get('tags', tags),
        #     attributes=payload.get('attributes', attributes),
        #     origin=payload.get('hostname', origin),
        #     raw_data=json.dumps(payload, indent=4)
        )

        # return Alert(
        #     resource=payload['resource'],
        #     event=payload['event'],
        #     environment=payload.get('environment', environment),
        #     severity=payload.get('severity', severity),
        #     service=['fail2ban'],
        #     group=payload.get('group', group),
        #     value='BAN',
        #     text=payload.get('message', text),
        #     tags=payload.get('tags', tags),
        #     attributes=payload.get('attributes', attributes),
        #     origin=payload.get('hostname', origin),
        #     raw_data=json.dumps(payload, indent=4)
        # )   

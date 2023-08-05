import logging

from events.generic_event import GenericEvent
from torch_client import TorchClient

logging.basicConfig(level=logging.INFO)

torchClient = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

pipeline = torchClient.get_pipeline('customer.orders.monthly.agg.pipeline')
pipeline_run = pipeline.get_latest_pipeline_run()
span_context = pipeline_run.get_span(span_uid='customer.orders.monthly.agg.pipeline.span')
print('sc : ', span_context)
span_context.send_event(GenericEvent(context_data={'dag_status': 'FAILED' },
                                    event_uid=f'customer.orders.monthly.agg.pipeline.span.error.event'))
span_context.failed(context_data={'dag_status': 'FAILED'})


import base64
import binascii
import gzip
import json
import os
import pprint
from datetime import datetime
from io import StringIO

import blackboxprotobuf
import httpx
import random
import requests
import time
from requests.structures import CaseInsensitiveDict


def protoTest():
    # protobuf_dict_with_data_from_burp
    pb = {"1": {"1": "9a8d2f0ce77a4e248bb71fefcb557637", "2": "be971928eab1bea3"},
          "101": {"1": "nk.vashisat@gmail.com", "2": "Crispy0500", "3": binascii.unhexlify("151515151515151515151515151515151515151515")}}

    # here you would want to edit the pb dict values, for example set new email
    pb['101']['1'] = "coool6@vool.online"
    pb['101']['2'] = "password902861"

    # matching_protobuf_types_dict_from_burp !!!!! change type 'string' to 'bytes'
    types = {
        "1": {
            "name": "",
            "type": "message",
            "field_order": [
                [
                    "1",
                    0
                ],
                [
                    "2",
                    0
                ]
            ],
            "message_typedef": {
                "1": {
                    "name": "",
                    "type": "bytes",
                    "example_value_ignored": "9a8d2f0ce77a4e248bb71fefcb557637"
                },
                "2": {
                    "name": "",
                    "type": "bytes",
                    "example_value_ignored": "1f1b44c5305af865"
                }
            }
        },
        "101": {
            "name": "",
            "type": "message",
            "field_order": [
                [
                    "1",
                    0
                ],
                [
                    "2",
                    0
                ],
                [
                    "3",
                    0
                ]
            ],
            "message_typedef": {
                "1": {
                    "name": "",
                    "type": "bytes",
                    "example_value_ignored": "akipon1970@gmail.com"
                },
                "2": {
                    "name": "",
                    "type": "bytes",
                    "example_value_ignored": "a1970124"
                },
                "3": {
                    "name": "",
                    "type": "bytes",
                    "example_value_ignored": "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                }
            }
        }
    }

    # encode the new
    print("--generating protobuf payload..")
    new_data = bytes(blackboxprotobuf.encode_message(pb, types))
    print()
    print("++protobuf_payload: ", new_data)

    # endpoint to send 'new_data' protobuf to
    url = "https://login5.spotify.com/v3/login"
    headers = {'Cache-Control': "no-cache, no-store, max-age=0",
               'User-Agent': "Spotify/8.7.36.905 Android/24 (Google Nexus 5X)",
               'Client-Token': "AABqQanaR1fJGNPQ/OQSyAtGMh50g6KDyRtx6iX/SdrNa5lpy5+1YjoOjdMePa0p+xq9NPvx5nH2JHC5uE5aC5RGYmxBbDUzlFVPklUZW1NlK0Kh7WgIAJg5p+bLUrwz3e0vozkEpUsvkyGhD6GXImZ0qJmacCqbgM22jrUQ4iq4GPjT8Aik5XDkGbXpoKhcgCLEE1M17P1wxaY5cISF17HFIyJdSXmKFeULjZTc8qBheg87zyrSznZLmnsTJKnUeuGPgfuuqObbRcnsvR6GmUyLoKrPTBX+6vp3+9HAe2y/YImbLFlg4Gkg",
               'Content-Type': "application/x-protobuf", 'Accept-Encoding': "gzip, deflate"}
    r = httpx.post(url, headers=headers, data=new_data)
    print("--request status: ", r.status_code)
    # decode 'r.content' the protobuf response with blackboxprotobuf
    message, typedef = blackboxprotobuf.protobuf_to_json(r.content)
    print(r.content)
    # load the message as JSON dict+
    message = json.loads(message)
    # print()
    print(message)
    # print()
    
    print( str(message['3']['1']['1']['1'],"utf-8"))

    # protobuf_dict_with_data_from_burp
    # pb = {"1": {"1": "9a8d2f0ce77a4e248bb71fefcb557637", "2": "1f1b44c5305af865"},
    #       "2": "\u0003\u0000d\u001d3(3\u00dc\u00b13\u00e1\u00ba\u009e\u0085\u001a\u00ead\u00ac8\u00e9c0\u00ba\u009b"
    #            "\u0018\u001e\u00d4\u009c\u0012\u00eb+Y.\u00c7\u00ef\u00cc\u0099\u00e7Ks\r\u008c\u0084\u00e4\u0014"
    #            "]\u00b0l7\u0015\t\u00ce\u00f9 "
    #            "\u00d3H\u0087yIN\"7\u008e\u0017g\u0081nZ\u00e0\u0099\u001f\u0088\u00ec1da4\u00e6a\u0015\u0016\u00b3"
    #            "\u0002Z\u00e7X\u00ad\u00ab\u00e1RW\u00c7'\u00eb\u00ad\u00a3\t\u00fe}\t\u00e9M\rj\u00b2\u0002\u00ad"
    #            "\u00d9 #:\u0006\u0080!\u008f\u008b\u0091\u00a998\u00da\u00e7R\u0099\u000f\u009d\u00f0\u00eb\u00b0/6"
    #            ":\u00e7\u00a0\u00aeC\u0088c\u00a4\u00e7\u00e7lo0\u000b\r\u00f5\u00ed?\u00cc\u00a9\u00b6\u00da\f\u00e9"
    #            "\u00ba9\u00a6y\u00af\u0000S&\u00e4\r\u000e\u00a7\u00b1\u0080\u0013Po\u0012\u0091\u0089\u00c8\u0090"
    #            "\u001c\u009f\u00e0\fn\u00aa\u00a6\u00d9\u0088\u00a9\u00d2oS\u00020\u00ee\u0084n\u00b4b9X{\u0001("
    #            "\u0001\u0007\u00f7\u00abGr\u008b\u00bb\u0098~\u00b0GC\u00dcH\u001c~\u0001J\u00ab\u00b2\u00c9\u00ec"
    #            "\u0001\u00f5\u0003\u00d9\u0004\u0002\u0011\u00cd\u0097\u00b3%\u00d3e:\u0011\u00d4",
    #       "3": {"1": {
    #           "1": {"1": "j\u00c6\u00eb\b\E\u00bb\\u0000\u0000\u0000\u0000\u0000\u0000\u0000_", "2": {"2": 543444}}}},
    #       "101": {"1": "akipon1970@gmail.com", "2": "a1970124", "3": "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"},
    #       '2': str(message['5'])}
    #
    # # here you would want to edit the pb dict values, for example set new email
    # pb['3']['1']['1']['1'] = str(message['3']['1']['1']['1'])
    # pb["2"] = str(message["5"])
    # pb['101']['1'] = "coool6@vool.online"
    # pb['101']['2'] = "password902861"
    #
    # # matching_protobuf_types_dict_from_burp !!!!! change type 'string' to 'bytes'
    # types = {
    #     "1": {
    #         "name": "",
    #         "type": "message",
    #         "field_order": [
    #             [
    #                 "1",
    #                 0
    #             ],
    #             [
    #                 "2",
    #                 0
    #             ]
    #         ],
    #         "message_typedef": {
    #             "1": {
    #                 "name": "",
    #                 "type": "bytes",
    #                 "example_value_ignored": "9a8d2f0ce77a4e248bb71fefcb557637"
    #             },
    #             "2": {
    #                 "name": "",
    #                 "type": "bytes",
    #                 "example_value_ignored": "1f1b44c5305af865"
    #             }
    #         }
    #     },
    #     "2": {
    #         "name": "",
    #         "type": "bytes",
    #         "example_value_ignored": "\u0003\u0000d\u001d`3(3\u00dc\u00b13\u00e1\u00ba\u009e\u0085\u001a\u00ead\u00ac8\u00e9c0\u00ba\u009b\u0018\u001e\u00d4\u009c\u0012\u00eb+Y.\u00c7\u00ef\u00cc\u0099\u00e7Ks\r\u008c\u0084\u00e4\u0014]\u00b0l7\u0015\t\u00ce\u00f9 \u00d3H\u0087yIN\"7\u008e\u0017g\u0081nZ\u00e0\u0099\u001f\u0088\u00ec1da4\u00e6a\u0015\u0016\u00b3\u0002Z\u00e7X\u00ad\u00ab\u00e1RW\u00c7'\u00eb\u00ad\u00a3\t\u00fe}\t\u00e9M\rj\u00b2\u0002\u00ad\u00d9 #:\u0006\u0080!\u008f`\u008b\u0091\u00a998\u00da\u00e7R\u0099\u000f\u009d\u00f0\u00eb\u00b0/6:\u00e7\u00a0\u00aeC\u0088c\u00a4\u00e7\u00e7lo0\u000b\r\u00f5\u00ed?\u00cc\u00a9\u00b6\u00da\f\u00e9\u00ba9\u00a6y\u00af\u0000S&\u00e4\r\u000e\u00a7\u00b1\u0080\u0013Po\u0012\u0091\u0089\u00c8\u0090\u001c\u009f\u00e0\fn\u00aa\u00a6\u00d9\u0088\u00a9\u00d2oS\u00020\u00ee\u0084n\u00b4b9X{\u0001(\u0001\u0007\u00f7\u00abGr\u008b\u00bb\u0098~\u00b0GC\u00dcH\u001c~\u0001J\u00ab\u00b2\u00c9\u00ec\u0001\u00f5\u0003\u00d9\u0004\u0002\u0011\u00cd\u0097\u00b3%\u00d3e:\u0011\u00d4"
    #     },
    #     "3": {
    #         "name": "",
    #         "type": "message",
    #         "field_order": [
    #             [
    #                 "1",
    #                 0
    #             ]
    #         ],
    #         "message_typedef": {
    #             "1": {
    #                 "name": "",
    #                 "type": "message",
    #                 "field_order": [
    #                     [
    #                         "1",
    #                         0
    #                     ]
    #                 ],
    #                 "message_typedef": {
    #                     "1": {
    #                         "name": "",
    #                         "type": "message",
    #                         "field_order": [
    #                             [
    #                                 "1",
    #                                 0
    #                             ],
    #                             [
    #                                 "2",
    #                                 0
    #                             ]
    #                         ],
    #                         "message_typedef": {
    #                             "1": {
    #                                 "name": "",
    #                                 "type": "bytes",
    #                                 "example_value_ignored": "j\u00c6\u00eb\b\\E\u00bb\\\u0000\u0000\u0000\u0000\u0000\u0000\u0000_"
    #                             },
    #                             "2": {
    #                                 "name": "",
    #                                 "type": "message",
    #                                 "field_order": [
    #                                     [
    #                                         "2",
    #                                         0
    #                                     ]
    #                                 ],
    #                                 "message_typedef": {
    #                                     "2": {
    #                                         "name": "",
    #                                         "type": "int",
    #                                         "example_value_ignored": 31595
    #                                     }
    #                                 }
    #                             }
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     "101": {
    #         "name": "",
    #         "type": "message",
    #         "field_order": [
    #             [
    #                 "1",
    #                 0
    #             ],
    #             [
    #                 "2",
    #                 0
    #             ],
    #             [
    #                 "3",
    #                 0
    #             ]
    #         ],
    #         "message_typedef": {
    #             "1": {
    #                 "name": "",
    #                 "type": "bytes",
    #                 "example_value_ignored": "akipon1970@gmail.com"
    #             },
    #             "2": {
    #                 "name": "",
    #                 "type": "bytes",
    #                 "example_value_ignored": "a1970124"
    #             },
    #             "3": {
    #                 "name": "",
    #                 "type": "bytes",
    #                 "example_value_ignored": "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    #             }
    #         }
    #     }
    # }
    #
    # # encode the new
    # print("--generating protobuf payload..")
    # new_data = bytes(blackboxprotobuf.encode_message(pb, types))
    # print("++protobuf_payload: ", new_data)
    #
    # # endpoint to send 'new_data' protobuf to
    # url = "https://login5.spotify.com/v3/login"
    # headers = {'Host': "login5.spotify.com", 'Cache-Control': "no-cache, no-store, max-age=0",
    #            'User-Agent': "Spotify/8.7.36.905 Android/24 (Google Nexus 5X)",
    #            'Client-Token': "AAD7RTT2HRZJJ3L7FSG95tAGBb3sTE607g3zwvryYkWilrkZcXoaFL10YD7lhCW8tHaWAnjL/z1qXDq9Sxm4C"
    #                            "+nDxVkYq4+1hDqoj4u+fCYKAlc6rlkWdcSvczOHrzMLWQHYAQOkZZ"
    #                            "/rBMN9Yy35NYGwk3DozR4SyRJoumI08hGyfUFaUHODto80EBghXJizOaDpIRLIMaZnL1p9t3IA5voBmfbtLBHmD6cU/tJorw7nEzGL1P+05L4V3vKBgSaBrCpmHCIM8R+ZSRsmHT8BOrcRfAUV4sEKDuV9rj/IH35AB4K6HKgDvTF6uDyKysUPOwHmFg==",
    #            'Content-Type': "application/x-protobuf", 'Accept-Encoding': "gzip, deflate"}
    # r = httpx.post(url, headers=headers, data=new_data)
    # print("--request status: ", r.status_code)
    # print(r.content)
    # # decode 'r.content' the protobuf response with blackboxprotobuf
    # message, typedef = blackboxprotobuf.protobuf_to_json(r.content)
    # # load the message as JSON dict
    # message = json.loads(message)
    # # print()
    # print(message)

def solvechallenge(login, prefix):
    pass

protoTest()

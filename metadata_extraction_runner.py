from metadata_extraction import lambda_handler

event = {

    'bucket': 'xyz-qwe',
    'key': 'kia2.jpg'

}

lambda_handler(event, None)

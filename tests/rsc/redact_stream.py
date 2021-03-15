import json
import argparse
import logging

logger = logging.getLogger()


def abridge_stream(stream_file_path):
    stream = []
    rec = None
    counter = 0
    with open(stream_file_path, 'r') as input:
        for line in input:
            l = json.loads(line)
            if l["type"] in ["STATE", "SCHEMA"]:
                stream.append(l)
            else:
                if rec != l["stream"]:
                    counter = 0
                    rec = l["stream"]
                else:
                    counter = counter + 1
                if counter <= 100:
                    stream.append(l)
    return stream


def redact_stream_generator(stream):
    if isinstance(stream, list):
        clean_stream = []
        for record in stream:
            record = record if isinstance(record, dict) or isinstance(record, list) else json.loads(record)
            if "type" in record and record.get("type") in ["STATE", "SCHEMA"]:
                yield record
            else:
                rec = record.get("record", record)
                for field, value in rec.items():
                    # print(f"inspecting {field} in {rec}")
                    if isinstance(value, dict):
                        # print(f"redacting dict {field}")
                        rec[field] = redact_stream(value)
                    elif isinstance(value, list):
                        arr = []
                        # print(f"redacting array {field}")
                        for item in value:
                            arr.append(redact_stream(item))
                        rec[field] = arr
                    elif field == "id" or field[-3:] == "_id":
                        # print(f"redacting {field}")
                        rec[field] = "redacted"
                    if "type" in record and record.get("type") == "RECORD" and "record" in record:
                        record["record"] = rec

                if "type" in record and record.get("type") == "RECORD":
                    yield record
                else:
                    clean_stream.append(rec)
        return clean_stream
    elif isinstance(stream, dict):
        for field, value in stream.items():
            # print(f"inspecting {field} in {stream}")
            if isinstance(value, dict):
                # print(f"redacting dict {field}")
                stream[field] = redact_stream(value)
            elif isinstance(value, list):
                arr = []
                # print(f"redacting array {field}")
                for item in value:
                    arr.append(redact_stream(item))
                stream[field] = arr
            elif field == "id" or field[-3:] == "_id":
                # print(f"redacting {field}")
                stream[field] = "redacted"
            return stream
    else: # it's just a value, ie a value in an array
        return stream



def redact_stream(stream):
    if isinstance(stream, list):
        clean_stream = []
        for record in stream:
            record = record if isinstance(record, dict) or isinstance(record, list) else json.loads(record)
            if "type" in record and record.get("type") in ["STATE", "SCHEMA"]:
                clean_stream.append(record)
            else:
                rec = record.get("record", record)
                for field, value in rec.items():
                    # print(f"inspecting {field} in {rec}")
                    if isinstance(value, dict):
                        # print(f"redacting dict {field}")
                        rec[field] = redact_stream(value)
                    elif isinstance(value, list):
                        arr = []
                        # print(f"redacting array {field}")
                        for item in value:
                            arr.append(redact_stream(item))
                        rec[field] = arr
                    elif field == "id" or field[-3:] == "_id":
                        # print(f"redacting {field}")
                        rec[field] = "redacted"
                    if "type" in record and record.get("type") == "RECORD" and "record" in record:
                        record["record"] = rec

                if "type" in record and record.get("type") == "RECORD" and "record" in record:
                    clean_stream.append(record)
                # else:
                #     clean_stream.append(rec)
        return clean_stream
    elif isinstance(stream, dict):
        for field, value in stream.items():
            # print(f"inspecting {field} in {stream}")
            if isinstance(value, dict):
                # print(f"redacting dict {field}")
                stream[field] = redact_stream(value)
            elif isinstance(value, list):
                arr = []
                # print(f"redacting array {field}")
                for item in value:
                    arr.append(redact_stream(item))
                stream[field] = arr
            elif field == "id" or field[-3:] == "_id":
                # print(f"redacting {field}")
                stream[field] = "redacted"
            return stream
    else: # it's just a value, ie a value in an array
        return stream


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument("-i", "--input", help="Input should be the file path containing an exerpt of the stream to redact for testing", required=True)
    parser.add_argument("-o", "--output", help="File path for the redacted stream", required=True)
    args = parser.parse_args()

    input = args.input  # input 'facebook_stream.json'
    output = args.output # output '../tests/rsc/facebook_stream_2.json',

    logger.info(f"reading from file {input}")
    stream = abridge_stream(input)
    logger.info(f"redacting fields named 'id' or ending in '_id' from {input}")
    stream = redact_stream(stream)
    logger.info(f"writing redacted stream to {output}")
    with open(output, 'wb') as f:
        for row in stream:
            try:
                f.write(bytes(json.dumps(row)+"\n", 'utf-8'))
            except Exception as e:
                logger.error(e)
                raise
    logger.info("process complete")

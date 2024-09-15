#!/bin/bash
ab -n 200 -c 200 -p generate-data.json -T application/json https://hazear.xyz/api/v1/generate > generate-test.log

#!/bin/bash
echo "Copying product...."
rm -r wso2am-3.1.1-SNAPSHOT
rm wso2am-3.1.1-SNAPSHOT.zip
cp ../product-apim/modules/distribution/product/target/wso2am-3.1.1-SNAPSHOT.zip .
unzip wso2am-3.1.1-SNAPSHOT.zip
echo "Done...!"  

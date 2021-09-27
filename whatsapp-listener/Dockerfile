FROM public.ecr.aws/lambda/python:3.8

RUN curl -O https://lambda-insights-extension.s3-ap-northeast-1.amazonaws.com/amazon_linux/lambda-insights-extension.rpm && \
    rpm -U lambda-insights-extension.rpm && \
    rm -f lambda-insights-extension.rpm

# install dependecies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --pre gql[all] --target "${LAMBDA_TASK_ROOT}" && \
    pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# copy code
COPY src "${LAMBDA_TASK_ROOT}"

CMD ["main.handle_campaign"]
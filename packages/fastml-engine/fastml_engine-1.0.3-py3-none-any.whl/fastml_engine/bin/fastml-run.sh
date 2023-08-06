echo "starting!"
if [ ! -n "${SERVICE_PATH}" ];then
  echo "unknown env key SERVICE_PATH"
  exit 1
fi
#创建日志目录
mkdir -p ${SERVICE_PATH}/logs
ENGINE_DIR=`python3 -c "import fastml_engine;print(fastml_engine.__path__[0])"`
gunicorn -c ${ENGINE_DIR}/gunicorn.py -e SERVICE_PATH=${SERVICE_PATH} --chdir ${ENGINE_DIR} --daemon=True web:app
if [ $? -ne 0 ];then
  echo 'failed,please check logs'
  exit 1
fi
echo "done!"
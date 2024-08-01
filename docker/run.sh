docker run \
      --name wsod_transfer-container \
      --gpus all \
      -it \
      -e "color_prompt=yes" \
      -t \
      --shm-size 32g \
      --rm \
      -v $HOME/dissertacao/models/wsod_transfer:/local \
      -v $HOME/dissertacao/data:/data \
      wsod_transfer

# run offline validation
output_folder=$1
models=($output_folder/*.pth)
for model in "${models[@]}"; do
    result_dir=$output_folder/results/$(basename "$model" .pth)
    mkdir $result_dir
    python tools/test_net.py --config-file $output_folder/config.yml --ckpt $model OUTPUT_DIR $result_dir
done
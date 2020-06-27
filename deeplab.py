# This file summarises all the changes required to train DeepLab V3+ on a custom dataset 
# (Solar Farms, in this case).

# 1. dataset_generator.py
# Provide a description of the dataset (Line 101)
_SOLAR_FARM_INFORMATION = DatasetDescriptor(
    splits_to_sizes={
        'train': 495  # num of samples in images/training
        'val': 30,  # num of samples in images/validation
    },
    num_classes=2,
    ignore_label=255,
) 

# Register the dataset description under a name (Line 102)
_DATASETS_INFORMATION = {
    'cityscapes': _CITYSCAPES_INFORMATION,
    'pascal_voc_seg': _PASCAL_VOC_SEG_INFORMATION,
    'ade20k': _ADE20K_INFORMATION,
    'solarfarm': _SOLAR_FARM_INFORMATION # registered
}

# 2. get_dataset_colormap.py (Line 332)
def create_solar_label_colormap():
  """Creates a label colormap for the Solar Farms dataset.

  Returns:
    A colormap for visualizing segmentation results.
  """
  return np.asarray([
      [0,0,0],
      [255,0,0],
  ])

# 3. train_utils.py (Line 209)
# Variables that will not be restored. This is done because 
# the no. of classes in our dataset may be different
exclude_list = ['global_step', 'logits']
if not initialize_last_layer:
  exclude_list.extend(last_layers)

# 4. train.py (Line 260)
# Sampling Imbalance: Since the dataset may contain a large no. of images for one paricular class
# and very few for the other ones, the model trained can become strongly biased to one particular class.
# To avoid this imbalance, provide more weights to the less occuring class objects (to punish the model)
for output, num_classes in six.iteritems(outputs_to_num_classes):
  train_utils.add_softmax_cross_entropy_loss_for_each_scale(
      outputs_to_scales_to_logits[output],
      samples[common.LABEL],
      num_classes,
      ignore_label,
      loss_weight=[1.0, 4.0],
      upsample_logits=FLAGS.upsample_logits,
      hard_example_mining_step=FLAGS.hard_example_mining_step,
      top_k_percent_pixels=FLAGS.top_k_percent_pixels,
      scope=output)

# 5. train.sh (Training Configuration)
python deeplab/train.py \
    --logtostderr \
    --training_number_of_steps=3000 \
    --train_split="train" \
    --model_variant="xception_65" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --base_learning_rate=0.0001 \
    --momentum=0.95 \
    --weight_decay=0.00001 \
    --decoder_output_stride=4 \
    --train_crop_size=256,256 \
    --train_batch_size=8 \
    --dataset="solarfarm" \
    --tf_initial_checkpoint='PS-1/code/deeplab/pretrained/deeplabv3_pascal_trainval' \
    --train_logdir='PS-1/code/deeplab/logs/9' \
    --dataset_dir='PS-1/tf-record'

# 6. vis.sh (Inference)
python deeplab/vis.py \
    --logtostderr \
    --vis_split="val" \
    --model_variant="xception_65" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --vis_crop_size=256,256 \
    --dataset="solarfarm" \
    --colormap_type="solarfarm" \
    --checkpoint_dir='PS-1/code/deeplab/logs/9' \
    --vis_logdir='PS-1/vis9' \
    --dataset_dir='PS-1/tf-record'

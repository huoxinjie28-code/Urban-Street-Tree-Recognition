# Model settings
model_cfg = dict(
    backbone=dict(type='EfficientNetV2', arch='b0'),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        num_classes=4,
        in_channels=1280,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=(1, 5),
    ))

# dataloader pipeline
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
rand_increasing_policies = [
    dict(type='AutoContrast'),
    dict(type='Equalize'),
    dict(type='Invert'),
    dict(type='Rotate', magnitude_key='angle', magnitude_range=(0, 30)),
    dict(type='Posterize', magnitude_key='bits', magnitude_range=(4, 0)),
    dict(type='Solarize', magnitude_key='thr', magnitude_range=(256, 0)),
    dict(
        type='SolarizeAdd',
        magnitude_key='magnitude',
        magnitude_range=(0, 110)),
    dict(
        type='ColorTransform',
        magnitude_key='magnitude',
        magnitude_range=(0, 0.9)),
    dict(type='Contrast', magnitude_key='magnitude', magnitude_range=(0, 0.9)),
    dict(
        type='Brightness', magnitude_key='magnitude',
        magnitude_range=(0, 0.9)),
    dict(
        type='Sharpness', magnitude_key='magnitude', magnitude_range=(0, 0.9)),
    dict(
        type='Shear',
        magnitude_key='magnitude',
        magnitude_range=(0, 0.3),
        direction='horizontal'),
    dict(
        type='Shear',
        magnitude_key='magnitude',
        magnitude_range=(0, 0.3),
        direction='vertical'),
    dict(
        type='Translate',
        magnitude_key='magnitude',
        magnitude_range=(0, 0.45),
        direction='horizontal'),
    dict(
        type='Translate',
        magnitude_key='magnitude',
        magnitude_range=(0, 0.45),
        direction='vertical')
]
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='RandomResizedCrop',
        size=192,
        efficientnet_style=True,
        interpolation='bicubic'),
    dict(type='RandomFlip', flip_prob=0.5, direction='horizontal'),
    dict(
        type='RandAugment',
        policies=rand_increasing_policies,
        num_policies=2,
        total_level=10,
        magnitude_level=9,
        magnitude_std=0.5,
        hparams=dict(
            pad_val=[round(x) for x in img_norm_cfg['mean'][::-1]],
            interpolation='bicubic')),
    dict(
        type='RandomErasing',
        erase_prob=0.25,
        mode='rand',
        min_area_ratio=0.02,
        max_area_ratio=1 / 3,
        fill_color=img_norm_cfg['mean'][::-1],
        fill_std=img_norm_cfg['std'][::-1]),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img']),
    dict(type='ToTensor', keys=['gt_label']),
    dict(type='Collect', keys=['img', 'gt_label'])
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='CenterCrop',
        crop_size=224,
        efficientnet_style=True,
        interpolation='bicubic'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img']),
    dict(type='Collect', keys=['img'])
]

# train
data_cfg = dict(
    batch_size = 32,
    num_workers = 4,
    train = dict(
        pretrained_flag = True,
        pretrained_weights = 'D:/Awesome-Backbones/logs/EfficientNetV2/2024-05-16-01-44-56(seoul-1k-4classes)/Train_Epoch098-Loss0.835.pth',
        freeze_flag = False,
        freeze_layers = ('backbone',),
        epoches = 100,
    ),
    test=dict(
        ckpt = 'D:/Awesome-Backbones/logs/EfficientNetV2/2024-05-16-02-50-19(seoul-2.5k-4classes)/Train_Epoch097-Loss0.727.pth',
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'confusion'],
        metric_options = dict(
            topk = (1,3),
            thrs = None,
            average_mode='none'
    )
    )
)


# batch 32
# lr = 0.1 *32 /256
# optimizer
optimizer_cfg = dict(
    type='SGD',
    lr=0.1 * 32/256,
    momentum=0.9,
    weight_decay=1e-4)

# learning 
lr_config = dict(type='StepLrUpdater', step=2, gamma=0.973, by_epoch=True)
#lr_config = dict(type='StepLrUpdater', warmup='linear', warmup_iters=500, warmup_ratio=0.25,step=[30,60,90])
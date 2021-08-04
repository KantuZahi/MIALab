import sys
import os

import numpy as np
import SimpleITK as sitk

try:
    import exercise.helper as helper
except ImportError:
    # Append the MIALab root directory to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))
    import exercise.helper as helper


def load_image(img_path, is_label_img):
    # todo: load the image from the image path with the SimpleITK interface (hint: 'ReadImage')
    # todo: if 'is_label_img' is True use argument outputPixelType=sitk.sitkUInt8,
    #  else use outputPixelType=sitk.sitkFloat32

    pixel_type = None  # todo: modify here
    img_ = None  # todo: modify here

    return img_


def to_numpy_array(img_):
    # todo: transform the SimpleITK image to a numpy ndarray (hint: 'GetArrayFromImage')
    np_img_ = None  # todo: modify here

    return np_img_


def to_sitk_image(np_image, reference_img):
    # todo: transform the numpy ndarray to a SimpleITK image (hint: 'GetImageFromArray')
    # todo: do not forget to copy meta-information (e.g., spacing, origin, etc.) from the reference image
    #  (hint: 'CopyInformation')! (otherwise defaults are set)

    img_ = None  # todo: modify here
    # todo: ...

    return img_


def register_images(img_, label_img_, atlas_img_):
    registration_method = _get_registration_method(atlas_img_, img_)  # type: sitk.ImageRegistrationMethod
    # todo: execute the registration_method to the img (hint: fixed=atlas_img, moving=img)
    # the registration returns the transformation of the moving image (parameter img) to the space of
    # the atlas image (atlas_img)
    transform = None  # todo: modify here

    # todo: apply the obtained transform to register the image (img) to the atlas image (atlas_img)
    # hint: 'Resample' (with referenceImage=atlas_img, transform=transform, interpolator=sitkLinear,
    # defaultPixelValue=0.0, outputPixelType=img.GetPixelIDValue())
    registered_img_ = None  # todo: modify here

    # todo: apply the obtained transform to register the label image (label_img) to the atlas image (atlas_img), too
    # be careful with the interpolator type for label images!
    # hint: 'Resample' (with interpolator=sitkNearestNeighbor, defaultPixelValue=0.0,
    # outputPixelType=label_img.GetPixelIDValue())
    registered_label_ = None  # todo: modify here

    return registered_img_, registered_label_


def preprocess_rescale_numpy(np_img_, new_min_val, new_max_val):
    max_val = np_img_.max()
    min_val = np_img_.min()
    # todo: rescale the intensities of the np_img to the range [new_min_val, new_max_val]. Use numpy arithmetics only.
    rescaled_np_img = None  # todo: modify here

    return rescaled_np_img


def preprocess_rescale_sitk(img_, new_min_val, new_max_val):
    # todo: rescale the intensities of the img to the range [new_min_val, new_max_val] (hint: RescaleIntensity)
    rescaled_img = None  # todo: modify here

    return rescaled_img


def extract_feature_median(img_):
    # todo: apply median filter to image (hint: 'Median')
    median_img_ = None  # todo: modify here

    return median_img_


def postprocess_largest_component(label_img_):
    # todo: get the connected components from the label_img (hint: 'ConnectedComponent')
    connected_components = None  # todo: modify here

    # todo: order the component by ascending component size (hint: 'RelabelComponent')
    relabeled_components = None  # todo: modify here

    largest_component = relabeled_components == 1  # zero is background
    return largest_component


# --- DO NOT CHANGE
def _get_registration_method(atlas_img_, img_) -> sitk.ImageRegistrationMethod:
    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.REGULAR)
    registration_method.SetMetricSamplingPercentage(0.2)

    registration_method.SetMetricUseFixedImageGradientFilter(False)
    registration_method.SetMetricUseMovingImageGradientFilter(False)

    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                      convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Set initial transform
    initial_transform = sitk.CenteredTransformInitializer(atlas_img_, img_,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)
    registration_method.SetInitialTransform(initial_transform, inPlace=False)
    return registration_method


# --- DO NOT CHANGE
if __name__ == '__main__':
    callback = helper.TestCallback()
    callback.start('SimpleITK')

    callback.start_test('load_image')
    img = load_image('../data/exercise/subjectX/T1native.nii.gz', False)
    load_ok = all((isinstance(img, sitk.Image),
                   img.GetPixelID() == 8,
                   img.GetSize() == (181, 217, 181),
                   img.GetPixel(100, 100, 100) == 12175,
                   img.GetPixel(100, 100, 101) == 11972))
    callback.end_test(load_ok)

    callback.start_test('to_numpy_array')
    np_img = to_numpy_array(img)
    to_numpy_ok = all((isinstance(np_img, np.ndarray),
                       np_img.dtype.name == 'float32',
                       np_img.shape == (181, 217, 181),
                       np_img[100, 100, 100] == 12175,
                       np_img[101, 100, 100] == 11972))
    callback.end_test(to_numpy_ok)

    callback.start_test('to_sitk_image')
    rev_img = to_sitk_image(np_img, img)
    to_sitk_ok = all((isinstance(rev_img, sitk.Image),
                      rev_img.GetOrigin() == img.GetOrigin(),
                      rev_img.GetSpacing() == img.GetSpacing(),
                      rev_img.GetDirection() == img.GetDirection(),
                      rev_img.GetPixel(100, 100, 100) == 12175,
                      rev_img.GetPixel(100, 100, 101) == 11972))
    callback.end_test(to_sitk_ok)

    callback.start_test('register_images')
    atlas_img = load_image('../data/exercise/mni_icbm152_t1_tal_nlin_sym_09a.nii.gz', False)
    label_img = load_image('../data/exercise/subjectX/labels_native.nii.gz', True)
    if isinstance(atlas_img, sitk.Image) and isinstance(label_img, sitk.Image):
        registered_img, registered_label = register_images(img, label_img, atlas_img)
        if isinstance(registered_img, sitk.Image) and isinstance(registered_label, sitk.Image):
            stats = sitk.LabelStatisticsImageFilter()
            stats.Execute(registered_img, registered_label)
            labels = stats.GetLabels()
            register_ok = all((registered_img.GetSize() == registered_label.GetSize() == (197, 233, 189),
                               labels == tuple(range(6))))
        else:
            register_ok = False
    else:
        register_ok = False
    callback.end_test(register_ok)

    callback.start_test('preprocss_rescale_numpy')
    if isinstance(np_img, np.ndarray):
        pre_np = preprocess_rescale_numpy(np_img, -3, 101)
        if isinstance(pre_np, np.ndarray):
            pre_np_ok = pre_np.min() == -3 and pre_np.max() == 101
        else:
            pre_np_ok = False
    else:
        pre_np_ok = False
    callback.end_test(pre_np_ok)

    callback.start_test('preprocss_rescale_sitk')
    pre_sitk = preprocess_rescale_sitk(img, -3, 101)
    if isinstance(pre_sitk, sitk.Image):
        min_max = sitk.MinimumMaximumImageFilter()
        min_max.Execute(pre_sitk)
        pre_sitk_ok = min_max.GetMinimum() == -3 and min_max.GetMaximum() == 101
    else:
        pre_sitk_ok = False
    callback.end_test(pre_sitk_ok)

    callback.start_test('extract_feature_median')
    median_img = extract_feature_median(img)
    if isinstance(median_img, sitk.Image):
        median_ref = load_image('../data/exercise/subjectX/T1med.nii.gz', False)
        if isinstance(median_ref, sitk.Image):
            min_max = sitk.MinimumMaximumImageFilter()
            min_max.Execute(median_img - median_ref)
            median_ok = min_max.GetMinimum() == 0 and min_max.GetMaximum() == 0
        else:
            median_ok = False
    else:
        median_ok = False
    callback.end_test(median_ok)

    callback.start_test('postprocess_largest_component')
    largest_hippocampus = postprocess_largest_component(label_img == 3)  # 3: hippocampus
    if isinstance(largest_hippocampus, sitk.Image):
        largest_ref = load_image('../data/exercise/subjectX/hippocampus_largest.nii.gz', True)
        if isinstance(largest_ref, sitk.Image):
            min_max = sitk.MinimumMaximumImageFilter()
            min_max.Execute(largest_hippocampus - largest_ref)
            post_ok = min_max.GetMinimum() == 0 and min_max.GetMaximum() == 0
        else:
            post_ok = False
    else:
        post_ok = False
    callback.end_test(post_ok)

    callback.end()

import pyclesperanto_prototype as cle

def segmentation(image, cells : cle.Image = None, sigma_noise_removal : float = 2, sigma_background_removal : float = 7, spot_detection_threshold : float = 10):
    from ..utils import stopwatch
    from ._background_subtraction import background_subtraction
    from ._spot_detection import spot_detection
    from ._cell_segmentation import cell_segmentation

    import time
    start_time = time.time()

    stopwatch()

    background_subtracted = None
    background_subtracted = background_subtraction(image, background_subtracted, sigma_noise_removal, sigma_background_removal)

    stopwatch("background subtraction")

    spots = cle.create_like(background_subtracted)
    spots = spot_detection(background_subtracted, spots, threshold=spot_detection_threshold)

    stopwatch("spot detect")

    if cells is None:
        cells = cle.create_like(spots)
    cells = cell_segmentation(spots, cells, number_of_dilations=14, number_of_erosions=8)

    stopwatch("cell segmentation")
    print("Segmentation took " + str(time.time() - start_time) + " s")

    return cells, spots


from magicgui import magicgui
from napari.layers import Image


@magicgui(
    auto_call=True,
    layout='vertical',
    sigma_noise_removal={'minimum': 0, 'maximum': 1000},
    sigma_background_removal={'minimum': 0, 'maximum': 1000},
    spot_detection_threshold={'minimum': 0, 'maximum': 100000},
)
def _segmentation(
        input1: Image = None,
        sigma_noise_removal: float = 1,
        sigma_background_removal: float = 15,
        spot_detection_threshold: float = 25,
        spots_only: bool = False
):
    import pyclesperanto_prototype as cle
    import beetlesafari as bs

    image = cle.push(input1.data)
    cells, spots = bs.segmentation(image, sigma_noise_removal=sigma_noise_removal,
                                   sigma_background_removal=sigma_background_removal,
                                   spot_detection_threshold=spot_detection_threshold)

    max_intensity = cle.maximum_of_all_pixels(cells)

    if spots_only:
        result = cle.pull(spots_only)
    else:
        result = cle.pull(cells)

    # show result in napari
    if (_segmentation.call_count == 0):
        _segmentation.self.viewer.add_labels(result, translate=input1.translate)
    else:
        _segmentation.self.layer.data = result
        _segmentation.self.layer.name = "Segmentation"
        _segmentation.self.layer.translate = input1.translate


from napari_pyclesperanto_assistant import Assistant


def attach_segmentation_dock_widget(assistant: Assistant):
    assistant.add_button("Beetlesafari segmentation", _segmentation)

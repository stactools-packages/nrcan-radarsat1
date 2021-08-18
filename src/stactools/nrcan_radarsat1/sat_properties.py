radarsat_product_characteristics = {
    "SCNA": "ScanSAR Narrow A",
    "SCNB": "ScanSAR Narrow B",
    "SCWA": "ScanSAR Wide A",
    "SCWB": "ScanSAR Wide B",
    "S1": "SAR Standard 1",
    "S2": "SAR Standard 2",
    "S3": "SAR Standard 3",
    "S4": "SAR Standard 4",
    "S5": "SAR Standard 5",
    "S6": "SAR Standard 6",
    "S7": "SAR Standard 7",
    "F1": "SAR Fine 1",
    "F2": "SAR Fine 2",
    "F3": "SAR Fine 3",
    "F4": "SAR Fine 4",
    "F5": "SAR Fine 5",
    "F1N": "SAR Fine 1N",
    "F2N": "SAR Fine 2N",
    "F3N": "SAR Fine 3N",
    "F4N": "SAR Fine 4N",
    "F5N": "SAR Fine 5N",
    "F1F": "SAR Fine 1F",
    "F2F": "SAR Fine 2F",
    "F3F": "SAR Fine 3F",
    "F4F": "SAR Fine 4F",
    "F5F": "SAR Fine 5F",
    "W1": "SAR Wide 1",
    "W2": "SAR Wide 2",
    "W3": "SAR Wide 3",
    "EH3": "SAR Extended High 1",
    "EH4": "SAR Extended High 2",
    "EH6": "SAR Extended High 3",
    "EL1": "SAR Extended Low 1"
}

radarsat_1_data_products = {
    "SLC": {
        "title":
        "Single Look Complex Product",
        "description":
        (f"The Single Look Complex (SLC) product differs from the SGF and SGX "
         f"products in that interpolation of the slant range coordinates is not performed into "
         f"ground range coordinates, and each image pixel is represented by complex I and Q "
         f"numbers to preserve the magnitude and phase information. SLC images can be generated "
         f"from any single beam mode. SLC image data is georeferenced as for SGF or SGX data, "
         f"but the range coordinate is in radar slant range rather than ground range. "
         f"Pixel sizes are variable and governed by the radar range and azimuth sampling rates. "
         f"All processing is single look; hence SLC products always provide imagery which utilises "
         f"the full available radar resolution, regardless of beam mode. Since SLC products retain "
         f"the phase information in the image data, they are useful in applications such as "
         f"pass-to-pass SAR interferometry."),
    },
    "SGF": {
        "title":
        "SAR Georeferenced Fine Resolution product (Path Image)",
        "description":
        (f"The SAR Georeferenced Fine Resolution (SGF) product is generated "
         f"with standard ground coordinate pixel dimensions of either 12.5m (for beams of Standard, "
         f"Wide, Extended Low and Extended High) or 6.25m (for Fine beam). With pixel size 12.5m, Standard "
         f"beams cover a nominal image dimension 100km square, and Wide beams cover 150km. "
         f"For Extended Low product, image dimensions are nominally 170km cross track by 100 to 170km "
         f"along track. For Extended High the image dimension is 75km square. All 12.5m pixel products "
         f"are the result of processing four independent azimuth samples, or four looks, in the along "
         f"track antenna beam dwell time, and then non-coherently summing the four looks prior to "
         f"forming the final image. This process results in smoothing of the coherent speckle noise in "
         f"the image to provide improved radiometric resolution for distributed or homogeneous target "
         f"areas. Typical spatial resolutions of these beams are in the order of 25m, i.e. twice the pixel size. "
         f"For Fine beam mode, the SGF pixel size is 6.25m and the nominal image dimension is 50km square. "
         f"The 6.25m pixel products are generated using the full available radar resolution, or one look, "
         f"in the along track antenna beam dwell time, to give spatial resolution of the order of 8m. "
         f"These products provide increased discrimination for discrete or point targets at the expense of "
         f"increased background speckle noise."),
    },
    "SGX": {
        "title":
        "SAR Georeferenced Extra Fine Resolution product (Path Image Plus)",
        "description":
        (f"The SAR Georeferenced Extra-Fine Resolution (SGX) products are generated "
         f"by denser sampling than the SGF products, in order to more fully utilize the resolution capabilities "
         f"of the SAR instrument. "
         f"  "
         f"The pixel sizes differ according to the beam mode: "
         f"* 8m pixel size for Standard and Extended High beam mode (4 looks); "
         f"* 10m pixel size for Wide and Extended Low beam mode (4 looks) and "
         f"* 3.125m pixel size for Fine beam mode (1 look). "
         f"  "
         f"The use of the smaller pixel dimensions compared with the SGF products ensures that the "
         f"image pixel dimensions do not exceed one half of the radar resolution for all regions of the "
         f"image. This is of significance in some applications where the best possible image resolution is "
         f"required, and where processing speed and volume of data product are secondary "
         f"considerations. Overall image scene dimensions for SGX products are the same as for the "
         f"corresponding SGF products. As an example, the basic radar ground range resolution for "
         f"Fine beam mode is of the order of 8m in both range and azimuth. In generating the 6.25m SGF "
         f"product, the data is undersampled relative to the usual Nyquist sampling criteria, "
         f"leading to a potential loss of information. The equivalent SGX product, with 3.125m sampling, "
         f"retains all of the input image information at the expense of a quadrupling of the volume of data. "
         ),
    },
    "SCN": {
        "title":
        "ScanSAR Narrow beam product",
        "description":
        (f"The ScanSAR Narrow (SCN) product is a georeferenced ground  coordinate "
         f"multi-look image produced by multiplexing either two (SNA) or three (SNB) single beams. "
         f"Image pixels are 25m square and scenes are nominally 300km in  the cross track (range) "
         f"dimension. The along track (azimuth) scene dimension is user selectable. SCN products are "
         f"generated using two looks in range and two looks in azimuth for a nominal total of four looks. "
         ),
    },
    "SCW": {
        "title":
        "ScanSAR Wide beam product",
        "description":
        (f"The ScanSAR Wide (SCW) product is a georeferenced ground coordinate "
         f"multi-look imageproduced by multiplexing four single beams for both SWA and SWB. "
         f"Image pixels are 50m square and scenes are nominally 450 km for SWB and 500 km for SWA in "
         f"the cross track (range) dimension. The along track (azimuth) scene dimension is user "
         f"selectable. SCW products are generated using four looks in range and two looks in azimuth "
         f"for a nominal total of eight looks."),
    },
}

gmArrayFilter: Axiom chip data filter and visualization
========================================================


Usage
-----------

split merged chip file


    $ gmArray filter array-split \
        array.file split.dir --prefix prefix


filter chip data

    $ gmArray filter array-filer-web \
        --array-dir uploads/project/605b06231ac54fdcc821c83f \
        --array-dir public/publicData/array \
        --genome-dir /home/kent/data/gmap/gmapdb/data \
        --out-dir public/score/605b06431ac54fdcc821c845 \
        --array-annotation-dir public/array \
        --options '{"mutant":["mutant"],"wild":["wild"],"mutant_parent":[],"wild_parent":[],"array":"660K","child_max_na":0,"parent_max_na":1,"mutant_gt":"homozygous","wild_gt":"heterozygous","mutant_parent_gt":"homozygous","wild_parent_gt":"homozygous","strict":0,"density_window":1000000,"density_step":500000,"genomes":["CSv1.0","CSv2.0"]}'

# Developing an Optimization and Design Tool for Marine Engineering

Greetings, traveler!

Congratulations on your decision to continue work on this thesis. We wish you the best of luck.

If you follow the steps and tips outlined below, you may have an easier time :)

## Requirements

Backwards compatibility may exist with the required software, but the original version numbers are shown below, just in case.
- Python 3.9
- PyCharm Professional 2020.3.5
- Git 2.4.1
- numpy 1.19.1
- treelib 1.6.1
- pandas 1.2.3
- scipy 1.6.1

### Python
We recommend you install Python via the Windows store, as this allows for the least amount of confusion regarding the setup process.

### PyCharm Professional
You can download the latest version of PyCharm from https://www.jetbrains.com/pycharm/download. 
Sign up with your webb.edu email address to receive a free lifetime subscription to the Professional version.

### Git
Download and install via https://git-scm.com/download/win.
Make sure to install both the BASH and GUI versions.
PyCharm will play nice with Git and has its own GUI, but you can use the native Git software if you wish to do so.

### numpy, treelib, pandas, scipy
Install these via the "pip install" command on Windows CMD. This will only work once you install Python.

## Contribution

The most recent version of the code repository is available on GitHub at https://github.com/alekoz47/electrical-systems-model.
Clone the most recent version of the repository by entering "git clone https://github.com/alekoz47/electrical-systems-model.git" in Git BASH.
Please create your own GitHub account and FORK the repository on your account to contribute.

See the network graph on the GitHub page at Insights->Network to see the branch history and setup.

### Current Branches
#### master
You should probably rename this too "main" to meet modern standards.
#### engine-loading
Contains in-progress work on the power plant optimization process.
Remaining work includes choosing optimization algorithms and testing the engine selection process that returns a Pareto front.
#### Holtrop
Contains in-progress work on estimating propulsion power requirements using the Holtrop method (check the paper for sources).
Remaining work includes testing and integrating this with the rest of the package.

## Usage

Most of this software is modular so feel free to use any portion of it that you would like.
It has yet to be packaged properly, so you will need to set it up in PyCharm or a similar IDE and install all dependencies to get it running.

The following are typical use cases with short directions:

### Modeling an electrical distribution system
```
epla_path = "../../tests/inputs/EPLA_example_1.csv"
load_cases = [0, 1, 2, 3, 4]
model = Model()
start = time.time()
model.load_epla(epla_path)
model.build()
model.print_tree()

root_powers = model.solve(load_cases)

cables = model.export_cables()

model.export_tree(show_cables=True)
model.export_tree(show_cables=False)
```

### Rating a set of engines over several loading conditions
```
at_sea = {
    'Name' : 'At Sea',
    'Mechanical Power': 0,
    'Electrical Power': 1000,
    'Use Factor': 0.75
    }

harbor = {
    'Name': 'Harbor',
    'Mechanical Power': 0,
    'Electrical Power': 500,
    'Use Factor': 0.15
    }

at_dock = {
    'Name': 'Dock',
    'Mechanical Power': 0,
    'Electrical Power': 100,
    'Use Factor': 0.10
    }

generator_1 = DieselGenerator([0, 0, 0], 1)
generator_2 = DieselGenerator([0, 0, 0], 1)
generator_3 = DieselGenerator([0, 0, 0], 1)

source_list = [generator_1, generator_2, generator_3]
load_cases = [at_sea, harbor, at_dock]
test_rater = EngineRatingSelector(source_list, load_cases)
```

### Generating a Pareto front set of rated engines
```
at_sea = {
    'Name' : 'At Sea',
    'Mechanical Power': 0,
    'Electrical Power': 1000,
    'Use Factor': 0.75
    }

harbor = {
    'Name': 'Harbor',
    'Mechanical Power': 0,
    'Electrical Power': 500,
    'Use Factor': 0.15
    }

at_dock = {
    'Name': 'Dock',
    'Mechanical Power': 0,
    'Electrical Power': 100,
    'Use Factor': 0.10
    }
    
selection = EngineSelector([at_sea, harbor, at_dock]
selection.run_optimization()
results = selection.results

fig = plt.figure()
points = [r["Objective"] for r in results]
plt.plot(points[0,:], points[1,:], '.r', markersize=16, )
plt.xticks([])
plt.yticks([])
plt.legend(loc=3, numpoints=1)
plt.show()
fig.set_size_inches(9.5, 6.5)
fig.savefig("bsfc_plot.png", dpi=800)
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Questions

Please reach out to the authors if you have any questions:
#### Alex Koziol 
akoziol21@webb.edu OR alekoz47@gmail.com
#### Ben Hunt 
bhunt21@webb.edu OR huntb802@gmail.com

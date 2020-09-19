from core.model import Model
from core.sink import ElectricalSink


def main():
    # test run of Motor -> Transformer -> Generator (root)
    # create data model
    # import data (this function currently uses test setup, no actual input implemented)
    # solve model
    model = Model()
    model.import_data("")
    print(model.solve_model())
    # TODO: add printout
    tree = model._sink_tree
    tree.show()

    # test adding some components and resolving
    motor2 = ElectricalSink([0, 0, 0], 2, 120, 0.8)
    motor2.name = "Motor 2"
    model.add_sink(motor2, 3)
    print(model.solve_model())
    tree.show()


if __name__ == "__main__":
    main()

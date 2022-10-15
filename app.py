from edge_layer.edge_controller import EdgeController

if __name__ == '__main__':
    try:
        #
        controller = EdgeController()
        controller.startListening()
    except KeyboardInterrupt:
        controller.stopListening()
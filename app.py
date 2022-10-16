from edge_layer.edge_controller import EdgeController, IngressMode

if __name__ == '__main__':
    try:
        controller = EdgeController(IngressMode.EdgeDataIngressMode.FileSystem)
        controller.startListening()
    except KeyboardInterrupt:
        controller.stopListening()
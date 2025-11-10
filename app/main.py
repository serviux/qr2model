"""
This application is a simple commandline program which takes a string input from a user, 
then generates a QR code and takes said code and converts it into a 3d model. 
"""


import argparse
from .qr_constructor_3d import QRGenerator3d
from .qr_constructor_3d import MeshConstructionParams

def validate_args(args:argparse.Namespace) -> bool:
    """Validates commandline arguments"""
    valid = True

    if args.message is  None:
        valid = False
        print("Message is required")
    return valid


def main():
    """Execution of the program"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--message", type=str, required=True,
                         help="the message to store in the QR code. The longer message the higher the version of the QR code will be")
    parser.add_argument("-d", "--depth", type=int, default=1,
                         help="the base depth of the mesh, for cells which are considered to be false")
    parser.add_argument("-t", "--true-depth", type=int, default=2,
                         help="the depth of the mesh for cells which are considered to be true")
    parser.add_argument("-s", "--size", type=int, default=1,
                         help="the height and width of each qr code square in the mesh")




    args  = parser.parse_args()
    if validate_args(args):
        params: MeshConstructionParams = MeshConstructionParams(size=args.size,
                                                                depth=args.depth,
                                                                true_depth=args.true_depth)
        qr_gen: QRGenerator3d = QRGenerator3d(params=params, qr_message=args.message)
        qr = qr_gen.generate_qr_code(args.message)
        mesh = qr_gen.construct_mesh(params, qr)
        qr_gen.save_mesh(mesh)

if __name__ == "__main__":
    main()
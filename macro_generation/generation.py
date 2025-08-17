import gdstk
import random
import math
length = 4  # Reduced from 8
avg_width = 1  # Reduced from 3
gap = 1  # Reduced from 1

min_metal6_width = 1.64  # Minimum Metal6 width in microns
min_metal6_spacing = 1.64 

# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library()

# Geometry must be placed in cells.
cell = lib.new_cell("my_logo")

# Use correct layer numbers for IHP SG13G2 PDK
# Layer 126 for TopMetal1 (artwork layer)
rect = gdstk.rectangle((2, 2), (10, 10), layer=126)
cell.add(rect)

# Add PR boundary (placement and routing boundary)
# Layer 189, datatype 4 for IHP SG13G2 PR boundary
pr_boundary = gdstk.rectangle((0, 0), (32, 32), layer=189, datatype=4)
cell.add(pr_boundary)


# Generate LEF file
def write_lef_file(filename, cell_name, cell_bounds, pins):
    """Write a LEF file for the cell"""
    with open(filename, 'w') as f:
        f.write("# LEF file generated for {}\n".format(cell_name))
        f.write("VERSION 5.8 ;\n")
        f.write("NAMESCASESENSITIVE ON ;\n")
        f.write("DIVIDERCHAR \"/\" ;\n")
        f.write("BUSBITCHARS \"[]\" ;\n")
        f.write("UNITS\n")
        f.write("   DATABASE MICRONS 1000 ;\n")
        f.write("END UNITS\n\n")
        
        # Define the cell
        f.write("MACRO {}\n".format(cell_name))
        f.write("   CLASS BLACKBOX ;\n")
        f.write("   FOREIGN {} 0 0 ;\n".format(cell_name))
        f.write("   SIZE {:.3f} BY {:.3f} ;\n".format(cell_bounds[2] - cell_bounds[0], cell_bounds[3] - cell_bounds[1]))
        f.write("   SYMMETRY X Y ;\n")
        
        # No pins - pure blackbox module for artwork
        
        f.write("END {}\n".format(cell_name))

# Calculate cell bounds (back to original size)
cell_width = 32  # 32 microns
cell_height = 32  # 32 microns
cell_bounds = (0, 0, cell_width, cell_height)

# Write LEF file
write_lef_file("../macros/my_logo.lef", "my_logo", cell_bounds, [])

# Save the library in a GDSII or OASIS file.
lib.write_gds("../macros/my_logo.gds")

# Optionally, save an image of the cell as SVG.
cell.write_svg("../macros/my_logo.svg")
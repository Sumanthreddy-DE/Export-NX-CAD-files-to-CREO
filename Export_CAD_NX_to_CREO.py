# NX Open Python script: Export one NX part file to STEP format
import os
import NXOpen

def main():
    # === USER INPUT SECTION ===
    input_part = r"Z:\Creo\Nov_6\prt_files\DIN_471_6X0D7.prt"
    output_step = r"Z:\Creo\Nov_6\STEP_files\DIN_471_6X0D7.stp"
    
    # === INITIALIZE NX SESSION ===
    session = NXOpen.Session.GetSession()
    lw = session.ListingWindow
    lw.Open()
    lw.WriteLine("=== NX STEP Export Script Started ===")

    part = None
    step_creator = None
    
    try:
        # Open the part
        lw.WriteLine("Opening part...")
        part, part_load_status = session.Parts.OpenBaseDisplay(input_part)
        if part_load_status:
            part_load_status.Dispose()
        
        session.Parts.SetDisplay(part, False, False)
        lw.WriteLine(f"✓ Opened: {part.Name}")
        lw.WriteLine(f"  Part path: {part.FullPath}")
        
        # Count bodies
        body_count = 0
        for body in part.Bodies:
            body_count += 1
        lw.WriteLine(f"  Found {body_count} bodies in part")
        lw.WriteLine("")

        # Create STEP export object
        lw.WriteLine("Creating STEP exporter...")
        step_creator = session.DexManager.CreateStepCreator()
        
        # Set the input file (the part being exported)
        step_creator.InputFile = part.FullPath
        
        # Set output file
        step_creator.OutputFile = output_step
        
        # Set object types to export
        step_creator.ObjectTypes.Solids = True
        step_creator.ObjectTypes.Surfaces = True
        step_creator.ObjectTypes.Curves = False
        
        # Set export format (AP214)
        step_creator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
        
        # Set export source (from display part)
        step_creator.ExportFrom = NXOpen.StepCreator.ExportFromOption.DisplayPart
        
        # IMPORTANT: Set the selection scope to export entire assembly
        step_creator.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.EntireAssembly
        
        # Optional: Set other properties
        step_creator.FileSaveFlag = False  # We're doing export, not save
        step_creator.ColorAndLayers = True  # Preserve colors and layers
        
        lw.WriteLine("Export settings:")
        lw.WriteLine(f"  Input: {step_creator.InputFile}")
        lw.WriteLine(f"  Output: {step_creator.OutputFile}")
        lw.WriteLine(f"  Solids: {step_creator.ObjectTypes.Solids}")
        lw.WriteLine(f"  Export from: Display Part")
        lw.WriteLine(f"  Format: AP214")
        lw.WriteLine("")

        # Perform export
        lw.WriteLine("Performing STEP export...")
        nxobject1 = step_creator.Commit()
        lw.WriteLine("✓ Export command completed")
        lw.WriteLine("")

        # Verify file was created
        lw.WriteLine("Verifying export...")
        if os.path.exists(output_step):
            file_size = os.path.getsize(output_step)
            lw.WriteLine(f"✓✓✓ SUCCESS! STEP file created!")
            lw.WriteLine(f"  Location: {output_step}")
            lw.WriteLine(f"  Size: {file_size} bytes ({file_size/1024:.2f} KB)")
        else:
            lw.WriteLine(f"✗✗✗ ERROR: STEP file was NOT created!")
            lw.WriteLine(f"  Expected location: {output_step}")
            
            # Try to find if it was created elsewhere
            output_dir = os.path.dirname(output_step)
            lw.WriteLine(f"\nChecking directory: {output_dir}")
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                lw.WriteLine(f"Files in directory: {len(files)}")
                for f in files:
                    if f.endswith('.stp') or f.endswith('.step'):
                        lw.WriteLine(f"  Found STEP file: {f}")

    except Exception as e:
        lw.WriteLine(f"✗✗✗ ERROR OCCURRED: {e}")
        import traceback
        lw.WriteLine("Full traceback:")
        lw.WriteLine(traceback.format_exc())

    finally:
        # Clean up
        if step_creator is not None:
            try:
                step_creator.Destroy()
            except:
                pass
        
        # Close part
        if part is not None:
            try:
                # Try different close methods
                try:
                    part.Close(NXOpen.BasePart.CloseWholeTree.False_, 
                              NXOpen.BasePart.CloseModified.UseResponses, None)
                except:
                    try:
                        part.Close(0, 0, None)
                    except:
                        pass
                lw.WriteLine("Part closed successfully")
            except:
                pass
        
        lw.WriteLine("")
        lw.WriteLine("=== NX STEP Export Script Finished ===")
        lw.WriteLine(f"Expected output: {output_step}")

if __name__ == "__main__":
    main()
# NX 2306
# Journal created by settipalli on Thu Nov  6 11:46:05 2025 Mitteleuropäische Zeit

#
import math
import NXOpen
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: File->Export->STEP...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    stepCreator1 = theSession.DexManager.CreateStepCreator()
    
    stepCreator1.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    
    stepCreator1.ObjectTypes.Solids = True
    
    stepCreator1.InputFile = "Z:\\Creo\\Nov_6\\prt_files\\DIN_625_61800.prt"
    
    stepCreator1.OutputFile = "C:\\ProgramData\\DIN_625_61800.stp"
    
    theSession.SetUndoMarkName(markId1, "Export STEP File Dialog")
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Export STEP File")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Export STEP File")
    
    stepCreator1.OutputFile = "Z:\\Creo\\Nov_6\\DIN_625_61800.stp"
    
    stepCreator1.FileSaveFlag = False
    
    stepCreator1.LayerMask = "1-256"
    
    stepCreator1.ProcessHoldFlag = True
    
    nXObject1 = stepCreator1.Commit()
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Export STEP File")
    
    stepCreator1.Destroy()
    
    # ----------------------------------------------
    #   Menu: Tools->Predict Commands->Record Movie
    # ----------------------------------------------
    # ----------------------------------------------
    #   Menu: Tools->Movie->Record...
    # ----------------------------------------------
    # ----------------------------------------------
    #   Menu: Tools->Predict Commands->Stop Journal Recording
    # ----------------------------------------------
    # ----------------------------------------------
    #   Menu: Tools->Automation->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()
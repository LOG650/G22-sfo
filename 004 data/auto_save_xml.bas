Attribute VB_Name = "AutoSaveXML"
'
' LOG650 G22 — auto-save MS Project som MSPDI XML ved hvert save
'
' Installasjon:
'   1. Åpne prosjektfilen i MS Project
'   2. Trykk Alt+F11 (åpner VBA Editor)
'   3. File → Import File → velg auto_save_xml.bas
'   4. Double-click ThisProject i prosjekt-treet til venstre
'   5. Lim inn hendelseshåndtereren under (Project_AfterSave) i ThisProject
'   6. Save prosjektfilen som Enabled Macro-format (.mpp beholder VBA)
'
' Hendelse som må limes inn i ThisProject-modulen:
'
'   Private Sub Project_AfterSave(ByVal pj As MSProject.Project, ByVal Info As EventInfo)
'       AutoSaveXML.SaveAsMSPDIXML pj
'   End Sub
'
' Etter dette vil hver Ctrl+S lagre både .mpp OG en .xml-fil ved siden av.
' XML-filen er den Python-pipelinen på Mac-siden leser via VirtioFS.
'

Option Explicit

' Lagrer en MSPDI XML-kopi ved siden av .mpp-filen
Public Sub SaveAsMSPDIXML(ByVal pj As MSProject.Project)
    Dim mppPath As String
    Dim xmlPath As String
    Dim baseName As String

    mppPath = pj.FullName
    If Len(mppPath) = 0 Then Exit Sub  ' filen er ikke lagret enda

    ' Bytt ut .mpp med .xml (eller legg til .xml hvis annet format)
    If LCase(Right(mppPath, 4)) = ".mpp" Then
        xmlPath = Left(mppPath, Len(mppPath) - 4) & ".xml"
    ElseIf LCase(Right(mppPath, 4)) = ".xml" Then
        ' Allerede en XML-fil; ikke re-lagre (unngå rekursjon)
        Exit Sub
    Else
        xmlPath = mppPath & ".xml"
    End If

    ' Lagre som MSPDI XML. FileSaveAs bytter aktiv fil; vi bruker SaveCopyAs
    ' via Application-metoder for å beholde original åpen.
    On Error GoTo SaveErr
    FileSaveAs Name:=xmlPath, FormatID:="MSProject.MSPDI"
    ' Gjenåpne .mpp-filen etter SaveAs (FileSaveAs bytter aktiv fil til XML)
    FileOpen Name:=mppPath, ReadOnly:=False
    Exit Sub

SaveErr:
    MsgBox "Auto-save XML feilet: " & Err.Description, vbExclamation, _
           "LOG650 AutoSaveXML"
End Sub

' Manuell versjon du kan mappe til en knapp/hurtigtast (Tools → Macros)
Public Sub SaveXMLNow()
    SaveAsMSPDIXML ActiveProject
    MsgBox "XML lagret ved siden av .mpp-filen.", vbInformation, "LOG650"
End Sub

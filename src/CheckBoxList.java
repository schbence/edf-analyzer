import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
public class CheckBoxList extends JPanel
{
  public JCheckBox[] checkList;
  CheckBoxList(String[] listElements, ActionListener listener){
    setPreferredSize(new Dimension(80,600));

    checkList = new JCheckBox[listElements.length];

    setLayout(new BoxLayout(this,BoxLayout.Y_AXIS));

    for(int i=0; i<listElements.length; i++){
      JCheckBox cb = new JCheckBox(listElements[i],true);
      cb.setActionCommand("CHECK");
      cb.addActionListener(listener);
      checkList[i] = cb;
      add(checkList[i]);
    }
  }


  public boolean[] getChecks(){
    boolean[] checks = new boolean[checkList.length];
    for(int i=0;i<checkList.length;i++){
      if(checkList[i].isSelected()){
        checks[i] = true;
      }else{
        checks[i] = false;
      }
    }
    return checks;
  }

  public void setChecks(boolean[] checkNew){
    for(int i=0;i<checkNew.length;i++){
      if(checkNew[i]==true){
        checkList[i].setSelected(true);
      }else{
        checkList[i].setSelected(false);
      }
    }
  }



  public void setElements(String[] listElements){
    removeAll();
    checkList = new JCheckBox[listElements.length];
    for(int i=0; i<listElements.length; i++){
      JCheckBox cb = new JCheckBox(listElements[i],true);
      checkList[i] = cb;
      add(checkList[i]);
    }



  }
/*
  public static void main(String args[])
  {
    JFrame f = new JFrame("CheckBox Example");
    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    String[] labels = new String[]{"a","b","c","d"};
    String[] labels2 = new String[]{"a22","b33","c44","5d5"};

    f.setSize(400,400);
    CheckBoxList cblist = new CheckBoxList(labels);
    cblist.setElements(labels2);
    f.add(cblist);
    f.setVisible(true);
    System.out.println(cblist.getChecks()[0]);
  }
*/
}

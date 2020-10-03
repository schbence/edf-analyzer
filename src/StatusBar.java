import java.awt.*;
import javax.swing.*;
public class StatusBar extends JPanel {
  private JLabel info = new JLabel("READY");


  public StatusBar(){
    setPreferredSize(new Dimension(1044+80,30));
    setVisible(true);
    add(info);
  }
  public void setInfo(String text){
    info.setText(text);
    repaint();
  }
  public void loadingProject(){
    info.setText("Loading project");
  }
  public void loadingEDF(){
    info.setText("Loading EDF data");
  }
  public void ready(){
    info.setText("READY");
  }
}

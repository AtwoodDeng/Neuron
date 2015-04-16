package Source;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/**
 *
 * @author Ravi
 */
public class TicTacToe implements ActionListener {

    private int[][] winCombinations = new int[][] {
			{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, //horizontal wins
			{0, 3, 6}, {1, 4, 7}, {2, 5, 8}, //virticle wins
			{0, 4, 8}, {2, 4, 6}			 //diagonal wins
		};
    public JFrame window = new JFrame("Tic-Tac-Toe");
    private JButton buttons[] = new JButton[9];
    private String letter = "";
    public boolean win = false;
    private int compMove = 0;
    private int currentPlayer;
    private int plays;
    private int index = -2;
    private BufferedReader reader =
            new BufferedReader(new InputStreamReader(System.in));

    public TicTacToe(){
	/*Create Window*/
	window.setSize(300,225);
	window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	window.setLayout(new GridLayout(4,3));

	/*Add Buttons To The Window*/
	for(int i=0; i<=8; i++){
		buttons[i] = new JButton();
		window.add(buttons[i]);
		buttons[i].addActionListener(this);
	}
        JButton computerMove = new JButton("Nengo");
        window.add(computerMove);
        computerMove.addActionListener(this);
	/*Make The Window Visible*/
	//window.setVisible(true);
	}
    protected void init() {
        currentPlayer = 1;
        plays = 0;
        setCompMove(1);
    }
    public void actionPerformed(ActionEvent a) {
        /*Calculate whose turn it is*/
        if(getCurrentPlayer()== 1)
        {
                letter = "O";
                //setCompMove(1);

                if(getIndex()>=0)
                {
                    buttons[getIndex()].setText(letter);
                    buttons[getIndex()].setEnabled(false);
                    System.out.println("Index Recieved "+getIndex());
                    switchPlayers();
                    setCompMove(0);
                }
                else
                    System.out.println("Could not determine location." + getIndex());

        }
        else
        {
                letter = "X";
                
                /*Write the letter to the button and deactivate it*/
                JButton pressedButton = (JButton)a.getSource();
                pressedButton.setText(letter);
                pressedButton.setEnabled(false);
                switchPlayers();
                setCompMove(1);

        }
        /*Determine who won*/
        for(int i=0; i<=7; i++){
            if( buttons[winCombinations[i][0]].getText().equals(buttons[winCombinations[i][1]].getText()) &&
                    buttons[winCombinations[i][1]].getText().equals(buttons[winCombinations[i][2]].getText()) &&
                    buttons[winCombinations[i][0]].getText() != ""){
                    win = true;
            }
        }

        /*Show a dialog when game is over*/
        if(win == true){
                JOptionPane.showMessageDialog(null, letter + " wins the game!");
                playAgainDialog();
        } else if(plays == 9 && win == false){
                JOptionPane.showMessageDialog(null, "The game was tie!");
                playAgainDialog();
        }
	}

    public void playAgainDialog() {
        int response = JOptionPane.showConfirmDialog(null, "Do you want to play again?", "Confirm", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE);
        if(response == JOptionPane.YES_OPTION)   reset();
        else    System.exit(0);

	}
    public void reset() {
        for(int i=0; i<=8; i++){
                buttons[i].setText("");
                buttons[i].setEnabled(true);
        }
        win = false;
        plays = 0;
        setCurrentPlayer(1);
        setCompMove(0);
	}
    protected void switchPlayers() {
        if (getCurrentPlayer() == 1) {
            setCurrentPlayer(2);
        } else {
            setCurrentPlayer(1);
        }
        setPlays(getPlays() + 1);
    }

    protected String getRules() {
        StringBuilder builder = new StringBuilder();
        builder.append("Players take turns marking a square. Only squares \n");
        builder.append("not already marked can be picked. Once a player has \n");
        builder.append("marked three squares in a row, they win! If all squares \n");
        builder.append("are marked and no three squares are the same, a tied game is declared.\n");
        builder.append("Have Fun! \n\n");
        return builder.toString();
    }

    protected String getPrompt() {
        String prompt = "";
        try {
            prompt = reader.readLine();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        return prompt;
    }

    public int getCurrentPlayer() {
        return currentPlayer;
    }

    public void setCurrentPlayer(int currentPlayer) {
        this.currentPlayer = currentPlayer;
    }

    public int getPlays() {
        return plays;
    }

    public void setPlays(int plays) {
        this.plays = plays;
    }

    public String getSymbolAt(Integer index){
        return buttons[index].getText();
    }

    /**
     * @return the compMove
     */
    public int getCompMove() {
        return compMove;
    }

    /**
     * @param compMove the compMove to set
     */
    public void setCompMove(int compMove) {
        this.compMove = compMove;
    }

    /**
     * @return the index
     */
    public int getIndex() {
        return index;
    }

    /**
     * @param index the index to set
     */
    public void setIndex(int index) {
        //System.out.println("Index set to "+index);
        this.index = index;
    }
    public int CompMove(){
            int i = 0;
            while(!buttons[i].getText().isEmpty())
            {
               i++;
            }
            return i;
        }
}

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package Source;

/**
 *
 * @author Ravi
 */
public class Main {

    public void play(TicTacToe game) {
        System.out.println("Welcome! Tic Tac Toe is a two player game.");
        game.init();
        System.out.println();
        System.out.println(game.getRules());
        System.out.println();
        game.window.setVisible(true);
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Main main = new Main();
    }
}

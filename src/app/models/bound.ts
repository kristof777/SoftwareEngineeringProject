/**
 * Bound is an interface which stores an upper and lower bound.
 *
 * Main application of this interface is in the filter to declare a lower/upper price range.
 */
export interface Bound{
    // ?: = Optional field
    upper?: number;
    lower?: number;
}
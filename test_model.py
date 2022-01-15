import pytest
import model


@pytest.mark.parametrize('value,position,index',
 [
     (-1, 5, 'A4'),
     ('test', -4, 'C16'),
     (True, 0, 'Z2')
 ])
def test_cell_init(value, position, index):
    cell = model.Cell(value, position, index)
    assert cell.getValue() == value
    assert cell.getPosition() == position 
    assert cell.getIndex() == index

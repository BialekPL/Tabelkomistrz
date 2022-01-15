import pytest
import model

# Tests for Cell class

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


@pytest.mark.parametrize('new_value', [20, -2, 1.5, "tekst"])
def test_cell_setValue(new_value):
    cell = model.Cell(0, 0, 'A4')
    cell.setValue(new_value)
    assert cell.getValue() == new_value

@pytest.mark.parametrize('new_position', [0, -2, 3])
def test_cell_setPosition(new_position):
    cell = model.Cell(0, 0, 'A1')
    cell.setPosition(new_position)
    assert cell.getPosition() == new_position

@pytest.mark.parametrize('new_index', ['A1', 'B5', 'G15'])
def test_cell_setIndex(new_index):
    cell = model.Cell(0, 0, 'A4')
    cell.setIndex(new_index)
    assert cell.getIndex() == new_index

@pytest.mark.parametrize('key,value', [('bold', 1)])
def test_cell_setStyle(key, value):
    cell = model.Cell(0, 0, 'A4')
    cell.setStyle(key)
    assert cell.getStyles[key] == value

# Tests for Table class
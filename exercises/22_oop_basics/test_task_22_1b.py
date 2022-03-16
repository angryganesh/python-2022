import sys

import task_22_1b

sys.path.append("..")

from pyneng_common_functions import (check_attr_or_method, check_class_exists,
                                     check_pytest, stdout_incorrect_warning,
                                     unify_topology_dict)

check_pytest(__loader__, __file__)


def test_class_created():
    """
    Проверка, что класс создан
    """
    check_class_exists(task_22_1b, "Topology")


def test_attr_topology(topology_with_dupl_links):
    """Проверяем, что в объекте Topology есть атрибут topology"""
    top_with_data = task_22_1b.Topology(topology_with_dupl_links)
    check_attr_or_method(top_with_data, attr="topology")


def test_topology_normalization(topology_with_dupl_links, normalized_topology_example):
    """Проверка удаления дублей в топологии"""
    correct_topology = unify_topology_dict(normalized_topology_example)
    return_value = task_22_1b.Topology(topology_with_dupl_links)
    return_topology = unify_topology_dict(return_value.topology)
    assert (
        type(return_value.topology) == dict
    ), f"По заданию в переменной topology должен быть словарь, а не {type(top_with_data.topology).__name__}"
    assert len(correct_topology) == len(
        return_value.topology
    ), "После создания экземпляра, в переменной topology должна находиться топология без дублей"


def test_method_delete_link_created(
    topology_with_dupl_links, normalized_topology_example
):
    """Проверяем, что в объекте Topology есть метод delete_link"""
    norm_top = task_22_1b.Topology(normalized_topology_example)
    check_attr_or_method(norm_top, method="delete_link")


def test_method_delete_link(normalized_topology_example, capsys):
    """Проверка работы метода delete_link"""
    norm_top = task_22_1b.Topology(normalized_topology_example)
    delete_link_result = norm_top.delete_link(("R3", "Eth0/0"), ("SW1", "Eth0/3"))
    assert None == delete_link_result, "Метод delete_link не должен ничего возвращать"

    assert ("R3", "Eth0/0") not in norm_top.topology, "Соединение не было удалено"

    # проверка удаления зеркального линка
    norm_top.delete_link(("R5", "Eth0/0"), ("R3", "Eth0/2"))
    assert ("R3", "Eth0/2") not in norm_top.topology, "Соединение не было удалено"

    # проверка удаления несуществующего линка
    norm_top.delete_link(("R8", "Eth0/2"), ("R9", "Eth0/1"))
    out, err = capsys.readouterr()
    link_msg = "Такого соединения нет"
    assert (
        link_msg in out
    ), "При удалении несуществующего соединения, не было выведено сообщение 'Такого соединения нет'"

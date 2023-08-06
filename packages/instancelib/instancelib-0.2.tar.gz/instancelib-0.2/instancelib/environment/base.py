# Copyright (C) 2021 The InstanceLib Authors. All Rights Reserved.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import annotations

from typing import Generic, Iterable, Sequence, Tuple, TypeVar, Any
from abc import ABC, abstractmethod
from ..instances import InstanceProvider, Instance
from ..labels import LabelProvider

from ..typehints import KT, DT, VT, RT, LT

InstanceType = TypeVar("InstanceType", bound="Instance[Any, Any, Any, Any]", covariant=True)
class AbstractEnvironment(ABC, Generic[InstanceType, KT, DT, VT, RT, LT]):
    @abstractmethod
    def create_empty_provider(self) -> InstanceProvider[InstanceType, KT, DT, VT, RT]:
        """Use this method to create an empty `InstanceProvider`

        Returns
        -------
        InstanceProvider[KT, DT, VT, RT]
            The newly created provider
        """        
        raise NotImplementedError

    @property
    @abstractmethod
    def dataset(self) -> InstanceProvider[InstanceType, KT, DT, VT, RT]:
        """This property contains the `InstanceProvider` that contains
        the original dataset. This provider should include all instances
        that are contained in the other providers.

        Returns
        -------
        InstanceProvider[KT, DT, VT, RT]
            The dataset `InstanceProvider`
        """        
        raise NotImplementedError

    @property
    @abstractmethod
    def all_datapoints(self) -> InstanceProvider[InstanceType, KT, DT, VT, RT]:
        """This provider should include all instances in all providers.
        If there are any synthethic datapoints constructed, they should be also 
         in here.

        Returns
        -------
        InstanceProvider[KT, DT, VT, RT]
            The dataset `InstanceProvider`
        """        
        raise NotImplementedError

    @property
    @abstractmethod
    def labels(self) -> LabelProvider[KT, LT]:
        """This property contains provider that has a mapping from instances to labels and
        vice-versa. 

        Returns
        -------
        LabelProvider[KT, LT]
            The label provider
        """        
        raise NotImplementedError

    def add_vectors(self, keys: Sequence[KT], vectors: Sequence[VT]) -> None:
        """This method adds feature vectors or embeddings to instances 
        associated with the keys in the first parameters. The sequences
        `keys` and `vectors` should have the same length.


        Parameters
        ----------
        keys : Sequence[KT]
            A sequence of keys
        vectors : Sequence[VT]
            A sequence of vectors that should be associated with the instances 
            of the sequence `keys`
        """        
        self.all_datapoints.bulk_add_vectors(keys, vectors)

    @abstractmethod
    def create_bucket(self, keys: Iterable[KT]) -> InstanceProvider[InstanceType, KT, DT, VT, RT]:
        raise NotImplementedError

    @abstractmethod
    def train_test_split(self,
                         source: InstanceProvider[InstanceType, KT, DT, VT, RT], 
                         train_size: int
                         ) -> Tuple[InstanceProvider[InstanceType, KT, DT, VT, RT], 
                                    InstanceProvider[InstanceType, KT, DT, VT, RT]]:
        raise NotImplementedError